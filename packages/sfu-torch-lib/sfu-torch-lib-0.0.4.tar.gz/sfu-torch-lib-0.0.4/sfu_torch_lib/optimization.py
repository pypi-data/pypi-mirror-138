import functools
from typing import Generator

import torch
import torch.autograd as autograd
from torch import Tensor
from torch.optim import Optimizer


def get_parameters(optimizer: Optimizer) -> Generator[Tensor, None, None]:
    yield from (
        parameter
        for parameter_group in optimizer.param_groups
        for _, parameters in parameter_group.items()
        for parameter in (parameters if isinstance(parameters, list) else [parameters])
        if torch.is_tensor(parameter) and parameter.requires_grad
    )


def manual_step(optimizer: Optimizer, loss: Tensor, allow_unused: bool = False) -> None:
    optimizer.zero_grad()

    parameters = list(get_parameters(optimizer))
    gradients = autograd.grad(loss, parameters, retain_graph=True, allow_unused=allow_unused)

    for parameter, gradient in zip(parameters, gradients):
        parameter.grad = gradient

    optimizer.step()
    optimizer.zero_grad()


def adaptive_clipping(optimizer: Optimizer, loss: Tensor, target_loss: Tensor, scale_factor: float) -> None:
    optimizer.zero_grad()

    parameters = list(get_parameters(optimizer))
    loss_gradients = autograd.grad(loss, parameters, retain_graph=True, allow_unused=True)
    target_gradients = autograd.grad(target_loss, parameters, retain_graph=True, allow_unused=True)

    target_norm, loss_norm = functools.reduce(
        lambda tuple_first, tuple_second: (tuple_first[0] + tuple_second[0], tuple_first[1] + tuple_second[1]),
        (
            (torch.sum(target_gradient ** 2), torch.sum(loss_gradient ** 2))
            for target_gradient, loss_gradient in zip(target_gradients, loss_gradients)
            if target_gradient is not None and loss_gradient is not None
        ),
    )
    target_norm, loss_norm = torch.sqrt(target_norm), torch.sqrt(loss_norm)

    scaling_factor = torch.minimum(loss_norm, target_norm) / loss_norm * scale_factor

    for parameter, target_gradient, loss_gradient in zip(parameters, target_gradients, loss_gradients):
        if target_gradient is not None:
            parameter.grad = target_gradient

        if loss_gradient is not None:
            if parameter.grad is not None:
                parameter.grad += scaling_factor * loss_gradient
            else:
                parameter.grad = loss_gradient

    optimizer.step()
    optimizer.zero_grad()
