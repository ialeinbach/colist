import sublime
import sublime_plugin
import re

class ColistCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # break a region into blocks
        blockify = re.compile(r'(?!\n).+?(?=\n{2,}|$)', re.DOTALL)

        # where to start regex search to find new blocks
        progress = 0 

        # do the same thing for each region
        for region in self.view.sel():
            # order of a, b not guaranteed
            forward = region.end() == region.b

            prev_block_end = 0

            while True:
                # get text of region
                content = self.view.substr(region)
                content_length = len(content)

                # find next block to format
                match = blockify.search(content, progress)
                if not match: break

                # extract block from region's text
                block_offset, block_end = match.start(), match.end()
                block = content[block_offset:block_end]

                # format block and update progress
                skew = self.update_block(edit, block_offset, block)
                progress += (block_end - block_offset) + skew + (block_offset - prev_block_end)

                # update region to take into account added spacing
                if forward:
                    region.b += skew
                else:
                    region.a += skew

                prev_block_end = block_end + skew

    def update_block(self, edit, block_offset, block):
        # make scaffold/skeleton of block
        rblock = reduce_block(block)

        num_lines = len(rblock)

        # finds where in region to add padding and how much padding to add
        def assess_line(ln, col, target, skew):
            nonlocal block_offset, rblock

            line_offset, line_content = rblock[ln][0], rblock[ln][1]
            delim_offset = line_content[col][0] + skew[ln]

            offset = block_offset + sum(skew[:ln]) + line_offset + delim_offset + 1
            padding = target - delim_offset + 1
            return offset, padding

        # tracks how much padding has been added per line
        skew = [0] * num_lines

        # aligns all lines in block by first column, then second, and so on
        for col in range(2):
            target = max_offset(rblock, col, skew)
        
            for ln in range(num_lines):
                offset, padding = assess_line(ln, col, target, skew)
                skew[ln] += self.view.insert(edit, offset, ' ' * padding)
        return sum(skew)

# extracts info about relative offsets of lines and commas within block
def reduce_block(block):
    lines = []

    start = 0

    # parse lines, reducing each as they are added to the list LINES
    for idx, char in enumerate(block):
        if char == '\n':
            lines.append([start, reduce_line(block[start:idx])])
            start = idx + 1
    if start < len(block):
        lines.append([start, reduce_line(block[start:len(block)])])

    return lines

# extracts info about relative offset of commas in line
def reduce_line(line):
    return [[ch, char] for ch, char in enumerate(line) if char == ',']

# calculates where to align a given column. assumes previous columns have been formatted.
def max_offset(rblock, col, skew):
    rightmost = 0
    for ln, line in enumerate(rblock):
        delim_offset = line[1][col][0] + skew[ln]
        if delim_offset > rightmost:
            rightmost = delim_offset
    return rightmost