
import onnx
import onnx.helper as helper
import onnx.onnx_pb
import google.protobuf.text_format as text_format
import numpy as np
import argparse

def clone_func(self):
    clone = onnx.onnx_pb.ModelProto()
    clone.CopyFrom(self)
    return clone

onnx.onnx_pb.ModelProto.Clone = clone_func

def node_to_string(node, array_prefix=None):
    if array_prefix is not None:
        vals = "\n".join(["  " + item for item in str(node).strip().split("\n")])
        return f"{array_prefix} {{\n{vals}\n}}"

    return str(node).strip()

def print_proto(proto, save_text=None, prefix=None):

    if proto is None:
        return

    text = None
    if hasattr(proto, "__len__"):
        if len(proto) > 0:
            for p in proto:
                if text is None:
                    text = node_to_string(p, prefix)
                else:
                    text += "\n" + node_to_string(p, prefix)
        else:
            print("Empty")
            return
    else:
        text = node_to_string(proto, prefix)

    if save_text is not None:
        open(save_text, "w").write(text)
    else:
        print(text)
    
def find_match(key, query):

    if isinstance(key, list):
        for k in key:
            if find_match(k, query):
                return True
        return False
    
    key = key.lower().strip()
    query = query.lower().strip()
    if key.find("*") == -1:
        return key == query

    key = key.replace("*", "")
    return query.find(key) != -1

def print_graph(model, node_name=None, op_type=None, input_name=None, output_name=None):

    if node_name is not None or op_type is not None or input_name is not None or output_name is not None:

        nodes = model.graph.node
        if node_name is not None:
            node_name_array = node_name.split(";")
            nodes = list(filter(lambda x:find_match(node_name_array, x.name), nodes))
            if len(nodes) == 0:
                print(f"Unknow node {node_name}, op_type {op_type}, input_name {input_name}, output_name {output_name}")
                return None

        if op_type is not None:
            op_type_array = op_type.lower().split(";")
            nodes = list(filter(lambda x:x.op_type.lower() in op_type_array, nodes))
            if len(nodes) == 0:
                print(f"Unknow node {node_name}, op_type {op_type}, input_name {input_name}, output_name {output_name}")
                return None

        def any_in(arra, arrb):
            for a in arra:
                if a in arrb:
                    return True
            return False

        if input_name is not None:
            input_name_array = input_name.lower().split(";")
            nodes = list(filter(lambda x:any_in(x.input, input_name_array), nodes))
            if len(nodes) == 0:
                print(f"Unknow node {node_name}, op_type {op_type}, input_name {input_name}, output_name {output_name}")
                return None

        if output_name is not None:
            output_name_array = output_name.lower().split(";")
            nodes = list(filter(lambda x:any_in(x.output, output_name_array), nodes))
            if len(nodes) == 0:
                print(f"Unknow node {node_name}, op_type {op_type}, input_name {input_name}, output_name {output_name}")
                return None

        return nodes, "node"

    nodes = list(filter(lambda x:x.op_type != "Constant", model.graph.node))
    while len(model.graph.node) > 0:
        model.graph.node.pop()

    model.graph.node.extend(nodes)
    while len(model.graph.initializer) > 0:
        model.graph.initializer.pop()

    return model.graph, "graph"

def print_with_nodeinput(model, input_name):
    
    if input_name is None: return model.graph.input
    input_name = input_name.split(";")
    nodes = []
    for node in model.graph.input:
        for item in input_name:
            if item == node.name:
                nodes.append(node)
                break
    
    return nodes

def print_with_nodeoutput(model, output_name):
    
    if output_name is None: return model.graph.output
    output_name = output_name.split(";")
    nodes = []
    for node in model.graph.output:
        for item in output_name:
            if item == node.name:
                nodes.append(node)
                break
    
    return nodes

def update_node(proto_graph, model_graph, method):

    if method == "full":
        if len(proto_graph.node) > 0:
            while len(model_graph.node) > 0:
                model_graph.node.pop()

            model_graph.node.extend(proto_graph.node)
    else:
        for n in proto_graph.node:
            for t in model_graph.node:
                if t.name == n.name:
                    t.CopyFrom(n)

def update_initializer(proto_graph, model_graph, method):

    if method == "full":
        if len(proto_graph.initializer) > 0:
            while len(model_graph.initializer) > 0:
                model_graph.initializer.pop()

            model_graph.initializer.extend(proto_graph.initializer)
    else:
        for n in proto_graph.initializer:
            for t in model_graph.initializer:
                if t.name == n.name:
                    t.CopyFrom(n)

def update_input(proto_graph, model_graph, method):

    if method == "full":
        if len(proto_graph.input) > 0:
            while len(model_graph.input) > 0:
                model_graph.input.pop()

            model_graph.input.extend(proto_graph.input)
    else:
        for n in proto_graph.input:
            for t in model_graph.input:
                if t.name == n.name:
                    t.CopyFrom(n)

def update_output(proto_graph, model_graph, method):

    if method == "full":
        if len(proto_graph.output) > 0:
            while len(model_graph.output) > 0:
                model_graph.output.pop()

            model_graph.output.extend(proto_graph.output)
    else:
        for n in proto_graph.output:
            for t in model_graph.output:
                if t.name == n.name:
                    t.CopyFrom(n)

def update_graph(model, file, save, phase, method="part"):

    if method not in ["part", "full"]:
        print(f"Unknow method {method}")
        return

    phase_map = {
        "graph": onnx.ModelProto,
        "node": onnx.GraphProto,
        "initializer": onnx.GraphProto,
        "input": onnx.GraphProto,
        "output": onnx.GraphProto
    }

    if phase not in phase_map:
        print(f"Unknow phase {phase}")
        return

    proto = phase_map[phase]()
    with open(file, "r") as f:
        text_format.Parse(f.read(), proto)

    if phase == "graph":
        for n, v in proto.graph.ListFields():
            if isinstance(v, (int, str, bytes, float)):
                setattr(model.graph, n.name, v)
        
        update_node(proto.graph, model.graph, method)
        update_initializer(proto.graph, model.graph, method)
        update_input(proto.graph, model.graph, method)
        update_output(proto.graph, model.graph, method)

    elif phase == "node":
        update_node(proto, model.graph, method)
    elif phase == "initializer":
        update_initializer(proto, model.graph, method)
    elif phase == "input":
        update_input(proto, model.graph, method)
    elif phase == "output":
        update_output(proto, model.graph, method)

    onnx.save_model(model, save)
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    s = parser.add_subparsers(dest="cmd")
    p = s.add_parser("graph", help="Print onnx graph")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("--node", default=None, type=str, help="需要打印的节点名称，如果多个，请用分号隔开，如果匹配，请加*，例如：a;b*;c")
    p.add_argument("--op", default=None, type=str, help="需要打印的节点optype，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--input", default=None, type=str, help="需要打印的节点optype，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--output", default=None, type=str, help="需要打印的节点optype，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--save", type=str, help="如果需要储存打印结果为文件，请指定文件名")

    p = s.add_parser("input", help="Print input")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("inputname", type=str, default=None, nargs="?", help="需要检索的input名称，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--save", type=str, help="如果需要储存打印结果为文件，请指定文件名")

    p = s.add_parser("output", help="Print output")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("outputname", type=str, default=None, nargs="?", help="需要检索的output名称，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--save", type=str, help="如果需要储存打印结果为文件，请指定文件名")

    p = s.add_parser("update", help="Update graph")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("--part", type=str, required=True, help="需要更新的part文件")
    p.add_argument("--phase", type=str, required=True, help="需要更新的part对应的阶段phase，graph、node、initializer、input、output")
    p.add_argument("--save", type=str, required=True, help="需要储存的新文件路径")
    p.add_argument("--method", type=str, default="full", help="更新所使用的方法，full=全替换，part=根据名称来更新")

    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        exit(0)

    model = onnx.load(args.onnxfile)

    if args.cmd == "graph":
        nd, prefix = print_graph(model, args.node, args.op, args.input, args.output)
        print_proto(nd, args.save, prefix)
    elif args.cmd == "input":
        print_proto(print_with_nodeinput(model, args.inputname), args.save, "input")
    elif args.cmd == "output":
        print_proto(print_with_nodeoutput(model, args.outputname), args.save, "output")
    elif args.cmd == "update":
        update_graph(model, args.part, args.save, args.phase)