
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

def to_lower_name(name):
    output = ""
    for i, a in enumerate(name):
        if i > 0 and ord(a) >= ord("A") and ord(a) <= ord("Z"):
            output += "_"
        output += a
    return output.lower()

def node_to_string(node, array_prefix=False):
    if array_prefix:
        name = to_lower_name(node.DESCRIPTOR.name[:-5])
        vals = "\n".join(["  " + item for item in str(node).strip().split("\n")])
        return f"{name} {{\n{vals}\n}}"

    return str(node).strip()

def print_proto(proto, save_text=None):

    if proto is None:
        return

    text = None
    if hasattr(proto, "__len__"):
        if len(proto) > 0:
            for p in proto:
                if text is None:
                    text = node_to_string(p, True)
                else:
                    text += "\n" + node_to_string(p, True)
        else:
            print("Empty")
            return
    else:
        text = node_to_string(proto, True)

    print(text)
    if save_text is not None:
        open(save_text, "w").write(text)
    
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

def print_graph(model, node_name=None, op_type=None):

    if node_name is not None or op_type is not None:

        nodes = model.graph.node
        if node_name is not None:
            node_name_array = node_name.split(";")
            nodes = list(filter(lambda x:find_match(node_name_array, x.name), nodes))
            if len(nodes) == 0:
                print(f"Unknow node {node_name}, op_type {op_type}")
                return None

        if op_type is not None:
            op_type_array = op_type.lower().split(";")
            nodes = list(filter(lambda x:x.op_type.lower() in op_type_array, nodes))
            if len(nodes) == 0:
                print(f"Unknow node {node_name}, op_type {op_type}")
                return None

        return nodes

    nodes = list(filter(lambda x:x.op_type != "Constant", model.graph.node))
    while len(model.graph.node) > 0:
        model.graph.node.pop()

    model.graph.node.extend(nodes)
    while len(model.graph.initializer) > 0:
        model.graph.initializer.pop()

    return model.graph

def print_with_nodeinput(model, input_name):
    
    if input_name is None: return model.graph.input
    input_name = input_name.split(";")
    nodes = []
    for node in model.graph.node:
        for item in input_name:
            if item in node.input:
                nodes.append(node)
                break
    
    return nodes

def print_with_nodeoutput(model, output_name):
    
    if output_name is None: return model.graph.output
    output_name = output_name.split(";")
    nodes = []
    for node in model.graph.node:
        for item in output_name:
            if item in node.output:
                nodes.append(node)
                break
    
    return nodes

def update_graph(model, file, save, phase):
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
        
        for n in proto.graph.node:
            for t in model.graph.node:
                if t.name == n.name:
                    t.CopyFrom(n)

        for n in proto.graph.initializer:
            for t in model.graph.initializer:
                if t.name == n.name:
                    t.CopyFrom(n)

        if len(proto.graph.input) > 0:
            while len(model.graph.input) > 0:
                model.graph.input.pop()
            model.graph.input.extend(proto.graph.input)

        if len(proto.graph.output) > 0:
            while len(model.graph.output) > 0:
                model.graph.output.pop()
            model.graph.output.extend(proto.graph.output)

    elif phase == "node":
        for n in proto.node:
            for t in model.graph.node:
                if t.name == n.name:
                    t.CopyFrom(n)
    elif phase == "initializer":
        for n in proto.initializer:
            for t in model.graph.initializer:
                if t.name == n.name:
                    t.CopyFrom(n)
    elif phase == "input":
        if len(proto.input) > 0:
            while len(model.graph.input) > 0:
                model.graph.input.pop()
            model.graph.input.extend(proto.input)
    elif phase == "output":
        if len(proto.output) > 0:
            while len(model.graph.output) > 0:
                model.graph.output.pop()
            model.graph.output.extend(proto.output)

    onnx.save_model(model, save)
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    s = parser.add_subparsers(dest="cmd")
    p = s.add_parser("graph", help="Print onnx graph")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("--node", default=None, type=str, help="需要打印的节点名称，如果多个，请用分号隔开，如果匹配，请加*，例如：a;b*;c")
    p.add_argument("--op", default=None, type=str, help="需要打印的节点optype，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--save", type=str, help="如果需要储存打印结果为文件，请指定文件名")

    p = s.add_parser("input", help="Print input")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("inputname", type=str, help="需要检索的input名称，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--save", type=str, help="如果需要储存打印结果为文件，请指定文件名")

    p = s.add_parser("output", help="Print output")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("outputname", type=str, help="需要检索的output名称，如果多个，请用分号隔开，例如：a;b;c")
    p.add_argument("--save", type=str, help="如果需要储存打印结果为文件，请指定文件名")

    p = s.add_parser("update", help="Update graph")
    p.add_argument("onnxfile", type=str, help="需要加载的onnx文件")
    p.add_argument("--part", type=str, required=True, help="需要更新的part文件")
    p.add_argument("--phase", type=str, required=True, help="需要更新的part对应的阶段phase，graph、node、initializer、input、output")
    p.add_argument("--save", type=str, help="需要储存的新文件路径")

    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        exit(0)

    model = onnx.load(args.onnxfile)

    if args.cmd == "graph":
        print_proto(print_graph(model, args.node, args.op), args.save)
    elif args.cmd == "input":
        print_proto(print_with_nodeinput(model, args.inputname), args.save)
    elif args.cmd == "output":
        print_proto(print_with_nodeoutput(model, args.outputname), args.save)
    elif args.cmd == "update":
        update_graph(model, args.part, args.save, args.phase)