import sys
import json

def call_graph(prog, pos=False):
    fns = prog['functions']
    # RI: f in call_graph[g] iff code for g calls f
    call_graph = {fn['name'] : [] for fn in fns}
    for function in prog['functions']:
        function_name = function['name']
        for instr in function['instrs']:
            if "label" in instr:
                continue
            elif instr['op'] == 'call':
                if pos and "pos" in instr:
                    call_graph[function_name].extend(
                        {
                            "callee_name" : func,
                            "pos" : instr["pos"],
                        }
                        for func in instr['funcs']
                    )
                else:
                    call_graph[function_name].extend(instr['funcs'])
    
    print(json.dumps(call_graph, indent=2))

if __name__ == '__main__':
    # copied from briltxt.py
    prog = json.load(sys.stdin)
    call_graph(prog, '-p' in sys.argv[1:])
