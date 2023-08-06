import svgwrite
from collections import namedtuple

class Dimensions:
    def __init__(self, grid_cols, grid_rows, max_text_size, max_label_width, legend_items):
        self.image_margin = 10
        self.character_height = 8
        self.character_width = 6.42 # tested with Chromium, hopefully it is the same in other software
        self.text_line_separation = 4
        self.square_margin = 4
        max_text_width, self.lines_cnt = max_text_size
        self.characters_cnt = max(max_text_width, max_label_width)
        self.stroke_width = 1
        self.square_height = self.square_margin + (self.character_height + self.text_line_separation) * self.lines_cnt + self.square_margin
        self.legend_height = self.square_margin + self.character_height + self.text_line_separation + self.square_margin
        self.square_width = self.square_margin + self.character_width * self.characters_cnt + self.square_margin
        self.grid_height = self.square_height * grid_rows
        self.grid_widht = self.square_width * max(grid_cols, len(legend_items))
        self.text_spacing = self.character_height + self.text_line_separation
        self.image_width = self.grid_widht + self.image_margin * 2
        self.image_height = self.grid_height + self.image_margin * 2
        if legend_items:
            self.image_height += self.legend_height + self.image_margin

class GridView:
    """Render dwo dimensional iterable into customized SVG image."""
    default_color = '#ffffff'
    """Color to be used when `color(e, x, y)` raises or returns `None`."""
    default_text = ''
    """Text to be used when `text(e, x, y)` raises."""
    flip_x = False
    """Whether or not to flip X axis."""
    flip_y = False
    """Whether or not to flip Y axis."""
    transpose = False
    """Whether or not to transpose entire data set."""
    legend = True
    """Whether or not to display legend. If legend is empty, it will be hidden anyway."""
    debug = False
    """Raise an exception if any element fails to provide color or text."""

    def __init__(self, target):
        """If target iterable `target` is mutable, it can be modified after creating instance of this class."""
        self._target = target

    def save(self, path):
        """Save SVG image into `path`."""
        grid, styles, max_text_size = self._wrap_elements()
        legend_items, max_label_width = self._build_legend(styles)
        grid_cols = len(grid)
        grid_rows = max(len(column) for column in grid)
        if self.transpose:
            grid_cols, grid_rows = grid_rows, grid_cols
        dim = Dimensions(grid_cols, grid_rows, max_text_size, max_label_width, legend_items)
        dwg_size = (dim.image_width, dim.image_height)
        dwg, dwg_styles = self._new_dwg(dim, styles, path, size=dwg_size)
        self._draw_grid(dwg, dim, dwg_styles, grid, legend_items)
        dwg.save()

    def text(self, e, x, y):
        """Abstract method that returns stringified version of element `e`. Coordinates are provided as `x` and `y`. If raises, `default_text` will be used. If returns `None`, `str(e)` will be used."""
        return None

    def color(self, e, x, y):
        """Abstract method that returns color assigned to element `e`. Coordinates are provided as `x` and `y`. Color should be HTML compatible, (e.g. `'#ff0000'` or `'red'`). Optionally color can be suffixed with label that builds up legend, e.g. `'#ff0000:foobar'`. If raises or returns `None`, `default_color` will be used.
        """
        return None

    def _wrap_elements(self):
        Element = namedtuple('Element', ['text_lines','style_index'])       
        styles = []
        max_text_lines = 1
        max_text_width = 1

        def wrap(element, x, y):            
            nonlocal styles
            nonlocal max_text_lines
            nonlocal max_text_width
            
            if self.transpose:
                x, y = y, x
            
            try:
                text = self.text(element, x, y)
                if text is None:
                    text = str(element)
            except Exception:
                if self.debug:
                    raise
                text = self.default_text
            
            text_lines = (text + '\n').splitlines()
            max_text_lines = max(max_text_lines, len(text_lines))
            max_text_width = max(max_text_width, max(len(line) for line in text_lines))

            try:
                color = self.color(element, x, y)
                if color is None:
                    style = (self.default_color, None)    
                else:
                    color_html, label, *_ = (*color.split(':'), None)
                    style = (color_html, label)
            except Exception as exc:
                if self.debug:
                    raise
                style = (self.default_color, None)

            try:
                style_index = styles.index(style)
            except ValueError:
                style_index = len(styles)
                styles.append(style)

            return Element(text_lines, style_index)

        grid_new = [[wrap(e, x, y) for y, e in enumerate(column)] for x, column in enumerate(self._target)]
        max_text_size = (max_text_width, max_text_lines)
        return grid_new, styles, max_text_size
    
    def _build_legend(self, styles):
        legend_items = {}
        max_label_width = 0
        if self.legend:
            for index, style in enumerate(styles):
                color_html, label = style
                if label is not None:
                    legend_items[label] = index
                    max_label_width = max(max_label_width, len(label))
        return legend_items, max_label_width

    def _build_styles(self, dwg, dim, styles):
        dwg_styles = {}
        css_styles = ''
        
        # Add new styles in order as corresponding layers appear on the drawing
        def new_style(index, classname, css):
            nonlocal css_styles
            dwg_styles[index] = dwg.add(dwg.g(class_=classname))
            css_code = '; '.join(name + ': ' + value for name, value in css.items())
            css_styles += '\n.' + classname + ' {' + css_code + '}'

        new_style('background', 'background', {'fill': '#eeeeee'})
        
        for index, style in enumerate(styles):
            color_html, label = style
            css = {'fill': color_html, 'stroke': 'black', 'stroke-width': f'{dim.stroke_width}pt'}
            new_style(index, f'style_{index}', css)
        
        css = {'font-family': 'monospace', 'font-size': f'{dim.character_height}pt'}
        new_style('text', 'text', css)

        return css_styles, dwg_styles
    
    def _new_dwg(self, dim, styles, path, size):
        dwg = svgwrite.Drawing(path, size=size)
        dwg.add(dwg.rect(size=('100%','100%'), class_='background'))
        css_styles, dwg_styles = self._build_styles(dwg, dim, styles)
        dwg.defs.add(dwg.style(css_styles))
        return dwg, dwg_styles
    
    def _draw_grid(self, dwg, dim, dwg_styles, grid, legend_items):
        text_style = dwg_styles['text']
        offset_x = offset_y = dim.image_margin
        
        if legend_items:
            for index, (label, style_index) in enumerate(legend_items.items()):
                xc = dim.image_margin + index * dim.square_width
                yc = dim.image_margin
                square = dwg.rect(insert=(xc, yc), size=(dim.square_width, dim.legend_height))
                dwg_styles[style_index].add(square)
                xc_text = xc + dim.square_margin
                yc_text = yc + dim.character_height + dim.square_margin
                text = dwg.text(label, insert=(xc_text, yc_text))
                text_style.add(text)
                
            offset_y += dim.legend_height + dim.image_margin
            
        for x, column in enumerate(grid):
            for y, element in enumerate(column):
                xv, yv = (y, x) if self.transpose else (x, y)
                
                xc = xv * dim.square_width
                if self.flip_x:
                    xc = dim.grid_widht - dim.square_width - xc
                xc += offset_x
                
                yc = yv * dim.square_height
                if self.flip_y:
                    yc = dim.grid_height - dim.square_height - yc
                yc += offset_y
                
                square = dwg.rect(insert=(xc, yc), size=(dim.square_width, dim.square_height))
                dwg_styles[element.style_index].add(square)

                for n, line in enumerate(element.text_lines):
                    xc_text = xc + dim.square_margin
                    yc_text = yc + dim.square_margin + dim.character_height + n * dim.text_spacing
                    text = dwg.text(line, insert=(xc_text, yc_text))
                    text_style.add(text)
