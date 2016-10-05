import time
import weakref
import random
import math
from deque import DynDeque
from sdl2 import Rect, init_everything, Keycode, Font
from sdl2.events import Quit, KeyDown
from dalgi import EntityGroup

class HighlightInfo:
    def __init__(self):
        self.block = None
        # What scope it is in at the end of the block
        self.parse_state_at_end = None
        """ TODO: add a way to flag that a preceding parse state has been dirtied,
        meaning that the following blocks must be recalculated (when they are
        drawn next time)"""

class TextBlock:
    def __init__(self):
        self.start = 0
        self.n_lines = 0
        self.n_wrapped_lines = 0

class Cursor:
    def __init__(self, line, col):
        self.line = line
        self.col = col

class EditorStyle:
    def __init__(self):
        self.margins = [5, 5, 5, 5]
        self.line_spacing = 1 # times the font's recommended spacing
        self.c_bg = None
        self.c_text = None
        self.c_sel = None

class EditorView:
    def __init__(self):
        self.style = None
        self.window = None # rect
        self.scroll_x = 0
        self.first_visible_line = 0
        self.y_offset_from_first_line = 0

"""class Editor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lines = [""]
        self.cursor = None"""
        

# get line from offset?
class Editor:
    SCROLL_SPEED_PPS = 100
    
    def __init__(self, text, rect, font, renderer, window_height):
        self.text_color = (0, 0, 0)
        self.bg_color = (0xF1, 0xF1, 0xF1)
        self.rect = rect
        self._y_offset = 0
        self.font = font
        self.lines = [line for line in text.splitlines()]
        self.spacing = int(round(font.line_skip() * 1.2))
        self.view_line = 0
        self.vy = 0
        self.max_lines = int(math.ceil(float(rect.h) / self.spacing)) + 1
        print("Max lines: {}".format(self.max_lines))
        self.line_textures = DynDeque(maxlen=self.max_lines)
        self.renderer = renderer
        self.texture_index = 0
        for line in self.lines[:self.max_lines]:
            self.line_textures.append(self.render_text(line))
    
    @property
    def y_offset(self):
        return self._y_offset
    
    @y_offset.setter
    def y_offset(self, value):
        max_offset = len(self.lines) * self.spacing
        self._y_offset = min(max(0, value), max_offset)
        #print("Setting offset to {} | max {} -> {}".format(value, max_offset, self._y_offset))
    
    def render_text(self, text):
        if not text or text.isspace():
            return None
        else:
            surf = self.font.render_blended(text, self.text_color)
            #surf = self.font.render_shaded(text, self.text_color, self.bg_color)
            tex = self.renderer.create_texture_from_surface(surf)
            return tex
    
    def update(self, dt):
        if self.vy:
            self.y_offset += self.vy * dt
    
    def update_line_textures(self, view_line):
        view_line = max(0, min(len(self.lines)-self.max_lines, view_line))
        if view_line == self.view_line: 
            return
        #print("Updating line textures...")
        if view_line < self.view_line:
            start = min(self.view_line - 1, view_line - 1 + self.max_lines)
            for lineno in range(start, view_line - 1, -1):
                if lineno >= len(self.lines):
                    break
                #print("- Adding line {}".format(lineno))
                self.line_textures.pop()
                self.line_textures.appendleft(self.render_text(self.lines[lineno]))
        else:
            for l in range(self.view_line, view_line):
                lineno = l + self.max_lines + 1
                if lineno >= len(self.lines):
                    break
                #print("- Adding line {}".format(lineno))
                self.line_textures.popleft()
                self.line_textures.append(self.render_text(self.lines[lineno]))
        
        self.view_line = view_line
    
    def draw(self, renderer, ox=0, oy=0):
        renderer.push_clip_rect(self.rect.moved_by(ox, oy))
        renderer.c_fill_rect(self.bg_color, self.rect.moved_by(ox, oy))
        # Load new lines
        new_view_line = int(math.floor(self.y_offset / self.spacing))
        self.update_line_textures(new_view_line)
        
        offset = int(math.floor(self.y_offset)) - (self.spacing * self.view_line)
        x = self.rect.x + ox
        y = self.rect.y + oy - offset
        for tex in self.line_textures:
            if tex is not None:
                dst = tex.rect_at(x, y)
                renderer.copy(tex, dst_rect=dst)
            y += self.spacing
        
        renderer.pop_clip_rect()
    
    def key_pressed(self, event):
        if event.keycode == Keycode.Down:
            self.vy += self.SCROLL_SPEED_PPS
        elif event.keycode == Keycode.Up:
            self.vy -= self.SCROLL_SPEED_PPS
        elif event.keycode == Keycode.Right:
            self.y_offset += self.rect.h
        elif event.keycode == Keycode.Left:
            self.y_offset = max(0, self.y_offset - self.rect.h)
    
    def key_released(self, event):
        if event.keycode == Keycode.Down:
            self.vy -= self.SCROLL_SPEED_PPS
        elif event.keycode == Keycode.Up:
            self.vy += self.SCROLL_SPEED_PPS

def main():
    """Entry point"""
    TIMEOUT = 0.001
    with init_everything() as context:
        window = context.build_window().title("Fauna").finish()
        renderer = window.build_renderer().finish()
        #renderer.set_clear_color(255, 255, 255)
        renderer.set_clear_color(*(220, 220, 220))
    
        #resources.load("resources.toml")
        
        group = EntityGroup()
        context.set_quit_handler(lambda: group.quit())
        
        font = Font.load("/System/Library/Fonts/Menlo.ttc", 12)
        with open("main.py") as f:
            text = f.read()
        rect = Rect(50, 50, 400, 400)
        editor = Editor(text, rect, font, renderer, 1000)
        group.add(editor)
        
        group.register_messages("TEST")
        META = None
        group.add(META)
        group.connect(META, "TEST", lambda: print("TEST RUN!"))
        group.validate_message_connections()
        
        group.init()
        last_frame = time.perf_counter()
        running = True
        while running:
            # handle events
            for event in context.get_events():
                group.handle(event)
                if type(event) == KeyDown and event.keycode == Keycode.Space:
                    group.send_message("TEST")
                
            # update
            now = time.perf_counter()
            delta_time = now - last_frame
            last_frame = now
            group.update(delta_time)
            #print("Deltatime: {}".format(delta_time))
            
            # render
            renderer.clear()
            predraw = time.perf_counter()
            group.draw(renderer)
            draw_delta = time.perf_counter() - predraw
            draw_fps = int(round(1.0 / draw_delta))
            #print("Drawing at {:04} FPS".format(draw_fps))
            
            renderer.present()
            
            # act nice
            time.sleep(TIMEOUT)
        
    
if __name__ == '__main__':
    main()
