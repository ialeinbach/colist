import sublime
import sublime_plugin
import re

class ColistCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        blockify = re.compile(r'(?!\n).+?(?=\n{2,}|$)', re.DOTALL)
        progress = 0

        for region in self.view.sel():
            forward = region.end() == region.b
            prev_block_end = 0
            while True:
                content = self.view.substr(region)
                content_length = len(content)

                match = blockify.search(content, progress)
                if not match: break

                block_offset = match.start()
                block_end = match.end()
                block = content[block_offset:block_end]

                skew = self.update_block(edit, block_offset, block)
                progress += len(block) + skew + (block_offset-prev_block_end)

                if forward:
                    region.b += skew
                else:
                    region.a += skew
                prev_block_end = block_end + skew

    def update_block(self, edit, block_offset, block):
        rblock = reduce_block(block)
        num_lines = len(rblock)

        def assess_line(ln, col, target, skew):
            nonlocal block_offset, rblock

            line_offset, line_content = rblock[ln][0], rblock[ln][1]
            delim_offset = line_content[col][0] + skew[ln]

            offset = block_offset + sum(skew[:ln]) + line_offset + delim_offset + 1
            padding = target - delim_offset + 1
            #print('line=%d,col=%d;offset=%d,padding=%d' % (ln, col, offset, padding))
            return offset, padding

        skew = [0] * num_lines
        for col in range(2):
            target = max_offset(rblock, col, skew)
        
            for ln in range(num_lines):
                offset, padding = assess_line(ln, col, target, skew)
                skew[ln] += self.view.insert(edit, offset, ' ' * padding)
        return sum(skew)

def reduce_block(block):
    lines = []

    start = 0
    for idx, char in enumerate(block):
        if char == '\n':
            lines.append([start, reduce_line(block[start:idx])])
            start = idx + 1
    if start < len(block):
        lines.append([start, reduce_line(block[start:len(block)])])

    return lines

def reduce_line(line):
    return [[ch, char] for ch, char in enumerate(line) if char == ',']

def max_offset(rblock, col, skew):
    rightmost = 0
    for ln, line in enumerate(rblock):
        delim_offset = line[1][col][0] + skew[ln]
        if delim_offset > rightmost:
            rightmost = delim_offset
    return rightmost