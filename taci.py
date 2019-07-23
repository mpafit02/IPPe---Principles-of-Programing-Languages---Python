import sys
import xml.etree.ElementTree as etree
import argparse

# Global Variables
assigned = dict()
instruction = list()
labels = dict()
pc_stack = list()
data_stack = list()


def main():
    instrCount = 0
    # Check the number of arguments
    if len(sys.argv) < 2:
        print("Error 99: Not enough arguments!")
        sys.exit(99)
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog='TACI', description='TACI Project Marios Pafitis')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('filename', metavar='filename',
                        type=str, help='Filename in XML')
    args = parser.parse_args()
    # Check if the XML is valid
    try:
        tree = etree.parse(args.filename)
    except:
        print('Error 3: Parsing Error during the parsing of XML, invalid XML input, file cannot be opened.', file=sys.stderr)
        sys.exit(3)
    root = tree.getroot()
    # Assign Labels
    for elem in root:
        if elem.attrib['opcode'] == 'LABEL':
            label(elem, instrCount)
        instruction.append(elem)
        instrCount += 1
    counter = 0
    # Execute the instructons
    while counter < instrCount:
        counter = controlOpCode(
            instruction[counter].attrib['opcode'], instruction[counter], counter)
        counter += 1
    # Just for Testing
    # print()
    # print('Assigned: ')
    # print(assigned)
    # print()
    # print('Commnads: ')
    # print(instruction)
    # print()
    # print('Labels: ')
    # print(labels)
    # print()
    # print('PC Stack: ')
    # print(pc_stack)
    # print()
    # print('Data Stack: ')
    # print(data_stack)
    # print()


def controlOpCode(opcode, elem, counter):
    dst = ''
    src1 = 0
    src2 = 0
    dst_type = ''
    # print(counter, ": " + opcode)
    if(opcode == 'MOV' or opcode == 'ADD' or opcode == 'SUB' or opcode == 'MUL' or opcode == 'DIV'
            or opcode == 'JUMPIFEQ' or opcode == 'PUSH' or opcode == 'CONCAT' or opcode == 'GETAT'
            or opcode == 'LEN' or opcode == 'STRINT' or opcode == 'INTSTR'):
        for subelem in elem:
            if subelem.tag == 'dst':
                dst = subelem.text
                dst_type = subelem.attrib['type']
            elif subelem.tag == 'src1' and subelem.attrib['kind'] == 'literal':
                src1 = subelem.text
            elif subelem.tag == 'src1':
                if assigned.__contains__(subelem.text):
                    src1 = assigned[subelem.text]
                else:
                    print(
                        'Error 11: Run-time Error: Read access to non-defined or non-initialized variable.', file=sys.stderr)
                    sys.exit(11)
            elif subelem.tag == 'src2' and subelem.attrib['kind'] == 'literal':
                src2 = subelem.text
            elif subelem.tag == 'src2':
                if assigned.__contains__(subelem.text):
                    src2 = assigned[subelem.text]
                else:
                    print(
                        'Error 11: Run-time Error: Read access to non-defined or non-initialized variable.', file=sys.stderr)
                    sys.exit(11)
        # print(src1)
        # print(src2)
    if opcode == 'MOV':
        mov(elem, dst, src1, dst_type)
    elif opcode == 'ADD':
        add(elem, dst, src1, src2)
    elif opcode == 'SUB':
        sub(elem, dst, src1, src2)
    elif opcode == 'MUL':
        mul(elem, dst, src1, src2)
    elif opcode == 'DIV':
        div(elem, dst, src1, src2)
    elif opcode == 'READINT':
        readint(elem, dst)
    elif opcode == 'PRINT':
        print_(elem)
    elif opcode == 'PRINTLN':
        println(elem)
    elif opcode == 'LABEL':
        return counter
    elif opcode == 'JUMP':
        return jump(elem, counter)
    elif opcode == 'JUMPIFEQ':
        return jumpifeq(elem, dst, src1, src2, counter)
    elif opcode == 'CALL':
        return call(elem, counter)
    elif opcode == 'RETURN':
        return return_(elem)
    elif opcode == 'PUSH':
        push(elem, src1)
    elif opcode == 'POP':
        pop(elem)
    elif opcode == 'READSTR':
        readstr(elem, dst)
    elif opcode == 'CONCAT':
        concat(elem, dst, src1, src2)
    elif opcode == 'GETAT':
        getat(elem, dst, src1, src2)
    elif opcode == 'LEN':
        len_(elem, dst, src1)
    elif opcode == 'STRINT':
        strint(elem, dst, src1)
    elif opcode == 'INTSTR':
        intstr(elem, dst, src1)
    else:
        print('Error 99: Wrong opcode!', opcode, file=sys.stderr)
        sys.exit(99)
    return counter


# ------------------MOV------------------
def mov(elem, dst, src1, dst_type):
    try:
        assigned[dst] = int(src1)
    except:
        print(
            'Error 14: Run-time Error: Operands of incompatible type.', file=sys.stderr)
        sys.exit(14)


# ------------------ADD------------------
def add(elem, dst, src1, src2):
    try:
        assigned[dst] = int(src1) + int(src2)
    except:
        print(
            'Error 14: Run-time Error: Operands of incompatible type.', file=sys.stderr)
        sys.exit(14)


# ------------------SUB------------------
def sub(elem, dst, src1, src2):
    try:
        assigned[dst] = int(src1) - int(src2)
    except:
        print(
            'Error 14: Run-time Error: Operands of incompatible type.', file=sys.stderr)
        sys.exit(14)


# ------------------MUL------------------
def mul(elem, dst, src1, src2):
    try:
        assigned[dst] = int(src1) * int(src2)
    except:
        print(
            'Error 14: Run-time Error: Operands of incompatible type.', file=sys.stderr)
        sys.exit(14)


# ------------------DIV------------------
def div(elem, dst, src1, src2):
    if int(src2) == 0:
        print(
            'Error 12: Run-time Error: Division by zero using DIV instruction.', file=sys.stderr)
        sys.exit(12)
    else:
        try:
            assigned[dst] = int(int(src1) / int(src2))
        except:
            print(
                'Error 14: Run-time Error: Operands of incompatible type.', file=sys.stderr)
            sys.exit(14)


# ------------------READINT------------------
def readint(elem, dst):
    data = input()
    for subelem in elem:
        if subelem.tag == 'dst':
            dst = subelem.text
            try:
                assigned[dst] = int(data)
            except:
                print(
                    'Error 13: Run-time Error: READINT get invalid value(not an integer).', file=sys.stderr)
                sys.exit(13)


# ------------------PRINT------------------
def print_(elem):
    for subelem in elem:
        if subelem.tag == 'src1' and subelem.attrib['kind'] == 'literal':
            print(subelem.text, end='')
        elif subelem.tag == 'src1':
            if assigned.__contains__(subelem.text):
                print(assigned[subelem.text], end='')


# ------------------PRINTLN------------------
def println(elem):
    print_(elem)
    print()


# ------------------LABEL------------------
def label(elem, count):
    for subelem in elem:
        if subelem.attrib['kind'] == 'literal' and subelem.attrib['type'] == 'string':
            if labels.__contains__(subelem.text):
                print(
                    'Error 5: Semantic Error during the semantic checks(e.g. a label occurs several times).', file=sys.stderr)
                sys.exit(5)
            else:
                labels[subelem.text] = count


# ------------------JUMP------------------
def jump(elem, counter):
    for subelem in elem:
        if subelem.tag == 'dst' and subelem.attrib['kind'] == 'literal':
            if labels.__contains__(subelem.text):
                return labels[subelem.text]
            else:
                print(
                    'Error 10: Run-time Error: Jump to a non-existing label or call to non-existing function.', file=sys.stderr)
                sys.exit(10)
    return counter


# ------------------JUMPIFEQ------------------
def jumpifeq(elem, dst, src1, src2, counter):
    try:
        if int(src1) == int(src2):
            if labels.__contains__(dst):
                # print('Is Equal -> Jump, Target is:', labels[dst])
                return labels[dst]
            else:
                print(
                    'Error 10: Run-time Error: Jump to a non-existing label or call to non-existing function.', file=sys.stderr)
                sys.exit(10)
    except:
        if str(src1) == str(src2):
            if labels.__contains__(dst):
                # print('Is Equal -> Jump, Target is:', labels[dst])
                return labels[dst]
            else:
                print(
                    'Error 10: Run-time Error: Jump to a non-existing label or call to non-existing function.', file=sys.stderr)
                sys.exit(10)
    # print('Is Not Equal -> Not Jump')
    return counter


# ------------------CALL------------------
def call(elem, counter):
    for subelem in elem:
        if subelem.tag == 'dst' and subelem.attrib['kind'] == 'literal':
            pc_stack.append(counter)
            if labels.__contains__(subelem.text):
                return labels[subelem.text]
            else:
                print(
                    'Error 10: Run-time Error: Jump to a non-existing label or call to non-existing function.', file=sys.stderr)
                sys.exit(10)
    return counter


# ------------------RETURN------------------
def return_(elem):
    try:
        return pc_stack.pop()
    except:
        print(
            'Error 15: Run-time Error: Pop from the empty (data/call) stack is forbidden.', file=sys.stderr)
        sys.exit(15)


# ------------------PUSH------------------
def push(elem, src1):
    data_stack.append(src1)


# ------------------POP------------------
def pop(elem):
    for subelem in elem:
        if subelem.tag == 'dst':
            dst = subelem.text
            try:
                data = data_stack.pop()
                # print(data)
                assigned[dst] = data
            except:
                print(
                    'Error 15: Run-time Error: Pop from the empty (data/call) stack is forbidden.', file=sys.stderr)
                sys.exit(15)


# ------------------READSTR-----------------
def readstr(elem, dst):
    data = input()
    for subelem in elem:
        if subelem.tag == 'dst':
            dst = subelem.text
            assigned[dst] = data


# ------------------CONCAT------------------
def concat(elem, dst, src1, src2):
    try:
        assigned[dst] = src1 + src2
    except:
        print(
            'Error 99: Can not concat not strings!', file=sys.stderr)
        sys.exit(99)


# ------------------GETAT------------------
def getat(elem, dst, src, i):
    s = list(src)
    try:
        pos = int(i)
        assigned[dst] = s[pos]
    except:
        print(
            'Error 20: Run-time Error: Can not convert string to integer!', file=sys.stderr)
        sys.exit(20)


# ------------------LEN------------------
def len_(elem, dst, src):
    assigned[dst] = len(src)


# ------------------STRINT------------------
def strint(elem, dst, src):
    try:
        assigned[dst] = int(src)
    except:
        print(
            'Error 20: Run-time Error: Can not convert string to integer!', file=sys.stderr)
        sys.exit(20)


# ------------------INTSTR------------------
def intstr(elem, dst, src):
    try:
        assigned[dst] = str(src)
    except:
        print(
            'Error 20: Run-time Error: Can not convert integer to string!', file=sys.stderr)
        sys.exit(20)


if __name__ == '__main__':
    main()
