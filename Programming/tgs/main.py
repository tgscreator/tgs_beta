import sys
import subprocess
from os import path
import shlex

iota_count = 0
def iota(reset=False):
    if reset:
        global iota_count
        iota_count = 0
    result = iota_count
    iota_count += 1
    return result

op_push=iota(True)
op_plus=iota()
op_minus=iota()
op_eq=iota()
op_if=iota()
op_end=iota()
op_else=iota()
op_dump=iota()
count_ops=iota()


def push(x):
    return (op_push, x)

def plus():
    return (op_plus, )

def dump():
    return (op_dump, )

def minus():
    return (op_minus, )

def equal():
    return (op_eq, )

def ifs():
    return (op_if, )

def ends():
    return (op_end, )

def elze():
    return (op_else, )

def simulate_program(program):
    stack = []
    ip = 0
    while ip < len(program):
        assert count_ops == 8, "Exhaustive handling of operations in simulation"
        op = program[ip]
        if op[0] == op_push:
            stack.append(op[1])
            ip += 1
        elif op[0] == op_plus:
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
            ip += 1
        elif op[0] == op_minus:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
            ip += 1
        elif op[0] == op_eq:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))
            ip += 1
        elif op[0] == op_if:
            a = stack.pop()
            if a == 0:
                assert len(op) >= 2, "'if' statements doesn't have a reference to the end of its' statement. Please call crefblock() on the prog before trying to simulate it."
                ip = op[1]
            else:
                ip += 1
        elif op[0] == op_end:
            ip += 1
        elif op[0] == op_dump:
            a = stack.pop()
            print(a)
            ip += 1
        else:
            assert False, "unreachable"

def compile_program(program, out_file_path):
    with open(out_file_path, "w") as out:
        out.write("BITS 64\n")
        out.write("segment .text\n")
        out.write("dump:\n")
        out.write("    mov     r9, -3689348814741910323\n")
        out.write("    sub     rsp, 40\n")
        out.write("    mov     BYTE [rsp+31], 10\n")
        out.write("    lea     rcx, [rsp+30]\n")
        out.write(".L2:\n")
        out.write("    mov     rax, rdi\n")
        out.write("    lea     r8, [rsp+32]\n")
        out.write("    mul     r9\n")
        out.write("    mov     rax, rdi\n")
        out.write("    sub     r8, rcx\n")
        out.write("    shr     rdx, 3\n")
        out.write("    lea     rsi, [rdx+rdx*4]\n")
        out.write("    add     rsi, rsi\n")
        out.write("    sub     rax, rsi\n")
        out.write("    add     eax, 48\n")
        out.write("    mov     BYTE [rcx], al\n")
        out.write("    mov     rax, rdi\n")
        out.write("    mov     rdi, rdx\n")
        out.write("    mov     rdx, rcx\n")
        out.write("    sub     rcx, 1\n")
        out.write("    cmp     rax, 9\n")
        out.write("    ja      .L2\n")
        out.write("    lea     rax, [rsp+32]\n")
        out.write("    mov     edi, 1\n")
        out.write("    sub     rdx, rax\n")
        out.write("    xor     eax, eax\n")
        out.write("    lea     rsi, [rsp+32+rdx]\n")
        out.write("    mov     rdx, r8\n")
        out.write("    mov     rax, 1\n")
        out.write("    syscall\n")
        out.write("    add     rsp, 40\n")
        out.write("    ret\n")
        out.write("global _start\n")
        out.write("_start:\n")
        for ip in range(len(program)):
            op = program[ip]
            assert count_ops == 7, "Exhaustive handling of operations in compilation"
            if op[0] == op_push:
                out.write("    ;; -- push %d --\n" % op[1])
                out.write("    push %d\n" % op[1])
            elif op[0] == op_plus:
                out.write("    ;; -- plus --\n")
                out.write("    pop rax\n")
                out.write("    pop rbx\n")
                out.write("    add rax, rbx\n")
                out.write("    push rax\n")
            elif op[0] == op_minus:
                out.write("    ;; -- minus --\n")
                out.write("    pop rax\n")
                out.write("    pop rbx\n")
                out.write("    sub rbx, rax\n")
                out.write("    push rbx\n")
            elif op[0] == op_dump:
                out.write("    ;; -- dump --\n")
                out.write("    pop rdi\n")
                out.write("    call dump\n")
            elif op[0] == op_eq:
                out.write("    ;; -- equal --\n")
                out.write("    mov rcx, 0\n");
                out.write("    mov rdx, 1\n");
                out.write("    pop rax\n");
                out.write("    pop rbx\n");
                out.write("    cmp rax, rbx\n");
                out.write("    cmove rcx, rdx\n");
                out.write("    push rcx\n")
            elif op[0] == op_if:
                out.write("    ;; -- if --\n")
                out.write("    pop rax\n")
                out.write("    test rax, rax\n")
                assert len(op) >= 2, "'if' statements doesn't have a reference to the end of its' statement. Please call crefblock() on the prog before trying to compile it."
                out.write("    jz addr_%d\n" % op[1])
            elif op[0] == op_end:
                out.write("addr_%d:\n" % ip)
            else:
                assert False, "unreachable"


        out.write("    mov rax, 60\n")
        out.write("    mov rdi, 0\n")
        out.write("    syscall\n")   

def parse_token_as_op(token):
    (file_path, row, col, word) = token
    assert count_ops == 8, "Exhaustive handling op in parse_token_as_op."
    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == 'print':
        return dump()
    elif word == '=':
        return equal()
    elif word == 'if':
        return ifs()
    elif word == 'end':
        return ends()
    elif word == 'else':
        return elze()
    else:
        try:
            return push(int(word))
        except ValueError as err:
            print("%s:%d:%d: %s" % (file_path, row, col, err))
            exit(1)

def crefblock(program):
    stack = []
    for ip in range(len(program)):
        op = program[ip]
        assert count_ops == 8, "Exhaustive handling of operations in crefblock. not all operators need to be handeled in here, only with statements"
        if op[0] == op_if:
            stack.append(ip)
        elif op[0] == op_else:
            if_ip = stack.pop()
            assert program[if_ip][0] == op_if, "'else' can only close 'if' statements"
            program[if_ip] = (op_if, ip)
            stack.append(ip)
        elif op[0] == op_end:
            statement_ip = stack.pop()
            if program[statement_ip][0] == op_if or program[statement_ip][0] == op_else:
                program[statement_ip] = (program[statement_ip][0], ip)
            else:  
                assert program[if_ip][0] == op_if, "'end' can only close 'if' statements right now."
    return program

def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start

def lex_line(line):
    col = find_col(line, 0, lambda x: not x.isspace())
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace())
        yield (col, line[col:col_end])
        col = find_col(line, col_end, lambda x: not x.isspace())         

def lex_file(file_path):
    with open(file_path, "r") as f:
        for (row, line) in enumerate(f.readlines()):
            for (col, token) in lex_line(line):
                yield (file_path, row, col, token)

def load_program_from_file(file_path):
    return crefblock([parse_token_as_op(token) for token in lex_file(file_path)])


def usage(program):
    print("Usage: %s <SUBCMD> [ARGS]", program)
    print("SUBCMDS")
    print("    sim  <file>      Simulate the program")
    print("    com  <file>      Compile the program")
    print("ERR: no subcmd was provided! Expected: 'sim' or 'com'")

def cmd_echos(cmd):
    print("[COMMANDS] %s" % " ".join(map(shlex.quote, cmd)))
    subprocess.call(cmd)


def call_cmd(cmd):
    print(cmd)
    subprocess.call(cmd)

def uncons(xs):
    return (xs[0], xs[1:])


if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) >= 1
    compiler_name, *argv = argv
    if len(argv) < 1:
        usage(program_name)
        print("ERR: No subcmd was provided! Expected: 'sim' or 'com'")
        exit(1)
    subcmd, *argv = argv

    if subcmd == "sim":
        if len(argv) < 1:
            usage(program_name)
            print("ERR: no input file is provided for the simulation.")
            exit(1)
        program_path, *argv = argv
        program = load_program_from_file(program_path)
        simulate_program(program)
    elif subcmd == "com":
        # TODO: -r flag fot com that runs the app
        if len(argv) < 1:
            usage(compiler_name)
            print("ERR: no input file is provided for the compilation.")
            exit(1)
        program_path, *argv = argv
        program = load_program_from_file(program_path);
        tgs_ext_path = '.tgs'
        basename = path.basename(program_path)
        if basename.endswith(tgs_ext_path):
            basename = basename[:-len(tgs_ext_path)]
        print("[INFO'S] Creating %s" % (basename + ".asm"))
        compile_program(program, basename + ".asm")
        cmd_echos(["nasm", "-felf64", basename + ".asm"])
        cmd_echos(["ld", "-o", basename, basename + ".o"])
    else:
        usage(compiler_name)
        print("ERROR: unknown SUBCMD %s" % (subcmd))
        exit(1)



