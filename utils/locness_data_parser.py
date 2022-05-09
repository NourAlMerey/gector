import json
import argparse


def apply_edits(original_text, edits):
    first_edit = 0
    modified_text = ""
    diff = 0
    for edit in edits:
        if first_edit == 0:
            modified_text = "%s%s%s" % (original_text[0:edit[0]], str(edit[2]), original_text[edit[1]:])
            first_edit += 1
        else:
            modified_text = "%s%s%s" % (modified_text[0:edit[0] + diff], str(edit[2]), modified_text[edit[1] + diff:])

        diff += len(str(edit[2])) - len(original_text[edit[0]:edit[1]])
    return modified_text


def process(file):
    data = []
    source = []
    target = []
    for line in open(file, 'r'):
        data.append(json.loads(line))

    for datum in data:
        source.append(datum['text'])
        target.append(apply_edits(datum['text'], datum['edits'][0][1]))
    return source, target


def write_to_file(source, target, sourcefile, targetfile):
    with open(sourcefile, 'w', encoding="utf-8") as source_file, open(targetfile, 'w',
                                                                               encoding="utf-8") as target_file:
        for s_line, t_line in zip(source, target):
            source_file.write('%s\n' % s_line)
            target_file.write('%s\n' % t_line)


def main(args):
    source, target = process(args.source)
    write_to_file(source, target, args.sourcefile, args.targetfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source',
                        help='Path to the json file',
                        required=True),
    parser.add_argument('-f1', '--sourcefile',
                        help='Path to the output source text file',
                        required=True)
    parser.add_argument('-f2', '--targetfile',
                        help='Path to the output target text file',
                        required=True)
    args = parser.parse_args()
    main(args)
