
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import extend_opview_class as _ods_extend_opview_class, segmented_accessor as _ods_segmented_accessor, equally_sized_accessor as _ods_equally_sized_accessor, get_default_loc_context as _ods_get_default_loc_context, get_op_result_or_value as _get_op_result_or_value, get_op_results_or_values as _get_op_results_or_values
_ods_ir = _ods_cext.ir

try:
  from . import _seq_ops_ext as _ods_ext_module
except ImportError:
  _ods_ext_module = None

import builtins


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "seq"
  pass


@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class CompRegOp(_ods_ir.OpView):
  OPERATION_NAME = "seq.compreg"

  _ODS_REGIONS = (0, True)

  def __init__(self, data, input, clk, name, reset, resetValue, innerSym, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(input))
    operands.append(_get_op_result_or_value(clk))
    if reset is not None: operands.append(_get_op_result_or_value(reset))
    if resetValue is not None: operands.append(_get_op_result_or_value(resetValue))
    attributes["name"] = name
    if innerSym is not None: attributes["innerSym"] = innerSym
    results.append(data)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def input(self):
    start, pg = _ods_equally_sized_accessor(operation.operands, 2, 0, 0)
    return self.operation.operands[start]

  @builtins.property
  def clk(self):
    start, pg = _ods_equally_sized_accessor(operation.operands, 2, 1, 0)
    return self.operation.operands[start]

  @builtins.property
  def reset(self):
    start, pg = _ods_equally_sized_accessor(operation.operands, 2, 2, 0)
    return self.operation.operands[start:start + pg]

  @builtins.property
  def resetValue(self):
    start, pg = _ods_equally_sized_accessor(operation.operands, 2, 2, 1)
    return self.operation.operands[start:start + pg]

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def innerSym(self):
    if "innerSym" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["innerSym"])

  @innerSym.setter
  def innerSym(self, value):
    if value is not None:
      self.operation.attributes["innerSym"] = value
    elif "innerSym" in self.operation.attributes:
      del self.operation.attributes["innerSym"]

  @innerSym.deleter
  def innerSym(self):
    del self.operation.attributes["innerSym"]

  @builtins.property
  def data(self):
    return self.operation.results[0]
