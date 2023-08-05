import torch
import collections

class ModuleHook(object):
    def __init__(self):
        super().__init__()
        # NOTE:
        # 1. module can be shared for different inputs and outputs (e.g. nn.ReLU in ResNet)
        # 2. functionals inputs and outputs are not collected (e.g. if using F.relu instead of nn.ReLU)
        # 3. inputs and outputs are not copied, so for an inplace operation, the final results are overwriten
        # Implementaton:
        # v1: use OrderedDict() for .modules, .inputs, .outputs
        # v2: use list of tuple for .modules, .inputs, .outputs
        # v3: use single list of dict
        self._info = [] # use list of dict to be extensable and allow duplicated keys

    def __call__(self, module, inputs, output):
        # NOTE: output = model(*inputs)
        # by default, inputs is tuple of tensors, output is a tensor
        # but inputs can be tuples of abitrary, output can be abitrary.
        # e.g. for MaskRCNN, input or output can be a tensor, int, float, string, None, OrderedDict, or Custom class (ImageList)

        # assert module.__name__ not in self.modules
        assert isinstance(inputs, tuple) # output = model(*inputs)
        self._info.append({'module_name': module.__name__,
            'module': module,
            'inputs': inputs,
            'output': output})

    def clear(self):
        self._info.clear()

    def __iter__(self):
        for item in self._info:
            yield item

    def register_extra_hook(self, name, func):
        for item in self._info:
            item[name] = func(item['module'], item['inputs'], item['output'])


class register_forward_hooks(object):
    def __init__(self, model, leaf_only=True):
        self.model = model
        self.leaf_only = leaf_only
        self.hook = ModuleHook()

    # def __call__(self, func):
    #     def inner(*args, **kwargs):
    #         with self:
    #             return func(*args, **kwargs)
    #     return inner

    def __enter__(self):
        from .utils import named_modules
        for name, mod in named_modules(self.model, leaf_only=self.leaf_only):
            mod.__name__ = name
            mod.register_forward_hook(self.hook)
        return self.hook

    def __exit__(self, *args):
        from .utils import unregister_all_hooks
        self.hook.clear()
        unregister_all_hooks(self.model)

def _module_type(mod, inputs, output):
    return type(mod).__name__

def _output_shape(mod, inputs, output):
    if torch.is_tensor(output):
        return tuple(output.shape)
    else:
        return () # not collected tensors in custom format

def _param_num(mod, inputs, output):
    if mod._modules:
        return 0  # not collected for non-leaf modules
    return sum([param.numel() for param in mod.parameters()])

def _flops(mod, inputs, output):
    """Calcluate FLOPs from module, inputs, and output.

    NOTE: currently only calculate _ConvNd and Linear layers."""
    import numpy as np
    shape = _output_shape(mod, inputs, output)
    if isinstance(mod, torch.nn.modules.conv._ConvNd):
        # (N*C_{l+1}*H*W)*C_l*K*K/G
        res = 1.0 * np.prod(shape) * mod.in_channels * np.prod(mod.kernel_size) / mod.groups
    elif isinstance(mod, torch.nn.Linear):
        res = 1.0 * np.prod(shape) * mod.in_features
    else:
        res = 0
    return int(res)

def _mem(mod, inputs, output):
    import numpy as np
    if hasattr(mod, 'inplace') and mod.inplace == True:
        res = 0
    else:
        shape = _output_shape(mod, inputs, output)
        res = 1.0 * np.prod(shape) * 4  # (in bytes, 1 float is 4 bytes)
    return int(res)

def _print_summary(model, *inputs):
    # use as torchtools.utils.print_summary
    with register_forward_hooks(model) as forward:
        model.eval()
        outputs = model(*inputs)
        forward.register_extra_hook('module_type', _module_type)
        forward.register_extra_hook('output_shape', _output_shape)
        forward.register_extra_hook('param_num', _param_num)
        forward.register_extra_hook('flops', _flops)
        forward.register_extra_hook('mem', _mem)

        def print_line(col_names, col_limits):
            print(' '.join([('{:>%d}' % n).format(s) for n, s in zip(col_limits, col_names)]))

        col_names = ['Layer (type)', 'Output shape', 'Param #', 'Flops', 'Memory (B)']
        col_limits = [40, 15, 12, 15, 12]
        total_limit = sum(col_limits) + len(col_limits) - 1
        # print head
        print('Model summary:')
        print(('-' * total_limit))
        print_line(col_names, col_limits)
        print(('=' * total_limit))
        # print inputs
        for x in inputs:
            if hasattr(x, 'shape'): # torch.Tensor or ndarray
                col_names = ['Input', 'x'.join(map(str, x.shape))]; print_line(col_names, col_limits)
        # print model leaf modules
        for _info in forward:
            col_names = ['{} ({})'.format(_info['module_name'], _info['module_type']),
                'x'.join(map(str, _info['output_shape'])),
                '{:,}'.format(_info['param_num']),
                '{:,}'.format(_info['flops']),
                '{:,}'.format(_info['mem'])]
            print_line(col_names, col_limits)
        print(('-' * total_limit))

        # print total
        total_params = sum([_info['param_num'] for _info in forward])
        total_params_with_aux = sum([p.numel() for p in model.parameters()])
        total_params_trainable = sum([p.numel() for p in model.parameters() if p.requires_grad])
        total_params_non_trainable = sum([p.numel() for p in model.parameters() if not p.requires_grad])
        total_flops = sum([_info['flops'] for _info in forward])
        print(('Total params: {:,} ({:,} MB)'.format(total_params, total_params * 4 / (1024 * 1024))))
        print(('Total params (with aux): {:,} ({:,} MB)'.format(total_params_with_aux, total_params_with_aux * 4 / (1024 * 1024))))
        print(('    Trainable params: {:,} ({:,} MB)'.format(total_params_trainable, total_params_trainable * 4 / (1024 * 1024))))
        print(('    Non-trainable params: {:,} ({:,} MB)'.format(total_params_non_trainable, total_params_non_trainable * 4 / (1024 * 1024))))
        print(('Total flops: {:,} ({:,} billion)'.format(total_flops, total_flops / 1e9)))
        print(('-' * total_limit))

        res = {'flops': total_flops, 'params': total_params, 'params_with_aux': total_params_with_aux}
    return res


def test_register_forward_hooks():
    import torchvision.models as models
    model = models.resnet18()

    with register_forward_hooks(model) as forward:
        inputs = torch.randn(1,3,224,224)
        outputs = model(inputs)
        forward.register_extra_hook('module_type', _module_type)
        forward.register_extra_hook('output_shape', _output_shape)
        forward.register_extra_hook('param_num', _param_num)
        forward.register_extra_hook('flops', _flops)
        forward.register_extra_hook('mem', _mem)

        for info in forward:
            print(info['module_name'], info['module_type'], info['output_shape'], info['param_num'], info['flops'], info['mem'])

    from torchtools.utils import named_modules
    for name, mod in named_modules(model, leaf_only=True):
        assert len(mod._forward_hooks) == 0

def test_print_summary():
    import torchvision.models as models
    model = models.resnet18()
    inputs = torch.randn(1,3,224,224)
    _print_summary(model, inputs)


if __name__ == "__main__":
    test_register_forward_hooks()
    test_print_summary()
