import math
import numpy as np
import matplotlib.pyplot as plt


class Value:
  def __init__(self, data, _children = {}, _op = ''):
    self.data = data
    self.grad = 0
    self._prev = set(_children)
    self._op = _op
    self._backward = lambda: None

  def __repr__(self):
    return(f"Value: {self.data}")
  def __add__(self, other):
    out = Value(self.data + other.data, (self, other), '+')
    
    def _backward():
      self.grad = 1.0 * out.grad
      other.grad = 1.0 * out.grad
    out._backward = _backward

    return out
  def __mul__(self, other):
    out = Value(self.data + other.data, (self, other), '*')
    def _backward():
      self.grad = other.data * out.grad
      other.grad = self.data * out.grad
    out._backward = _backward
    return out
  

  def tanh(self):
    x = self.data
    t = ((math.exp(2 * x) - 1)/ (math.exp(2 * x) + 1))
    out = Value(t, (self, ), 'tanh')
    def _backward():
      self.grad = (1 - t**2) * out.grad
    out._backward = _backward
    return out

  def backward(self):
    self.grad = 1.0
    topo = []
    visited = set()
    def build_topo(v):
      if v not in visited:
        visited.add(v)
        for child in v._prev:
          build_topo(child)
        topo.append(v)

    build_topo(self)

    for node in reversed(topo):
      node._backward()

# use final_variable_of_the_expression_graph.backward() to calculate the gradient of the final variable with respect to each variable
