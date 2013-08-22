#!/usr/bin/python
import inspect
import ast


class ReturnCallTransformer(ast.NodeTransformer):
    """ A class for transforming call nodes in an abstract syntax tree """
    target_name = None
    replacement = None
    target_argspec = None

    def __init__(self, target_name, replacement, target_argspec):
        self.target_name = target_name
        self.replacement = replacement
        self.target_argspec = target_argspec

    def visit_Return(self, node):
        """
        Replace an ast.Return(value=ast.Call) with our replacement if the call
        matches our target_name
        """
        if isinstance(node.value, ast.Call):
            if node.value.func.id == self.target_name:
                result = []

                function_arg_defaults = [] + self.target_argspec.defaults
                for arg in self.target_argspec.args:
                    arg_name = ast.Name(id=arg.id, ctx=ast.Store())
                    try:
                        arg_value = node.value.args.pop(0)
                    except IndexError:
                        arg_value = function_arg_defaults.pop(0)
                    result.append(ast.Assign(targets=[arg_name],
                                             value=arg_value))
                result.append(self.replacement)
                return result
        return node


def tct(infunc):
    """ Transform a recursive call to an iteration... in some cases """
    tree = ast.parse(inspect.getsource(infunc))
    transformer = ReturnCallTransformer(infunc.func_name,
                                        ast.Continue(),
                                        tree.body[0].args)
    trans_tree = transformer.visit(tree)

    trans_tree.body[0].body = [
        ast.While(test=ast.Name(id='True', ctx=ast.Load()),
                  body=trans_tree.body[0].body + [ast.Break()],
                  orelse=[])
    ]

    # remove TCT decorator, so that we only do TCT once
    trans_tree.body[0].decorator_list = [decorator for decorator
        in trans_tree.body[0].decorator_list if decorator.id != 'tct']

    outfunc_code = compile(ast.fix_missing_locations(trans_tree),
                           inspect.getfile(infunc), 'exec')

    eval_env = globals().copy()
    eval(outfunc_code, eval_env)
    return eval_env[infunc.func_name]
