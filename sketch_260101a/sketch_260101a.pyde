TREE_HEIGHT = 520
TREE_WIDTH = 300
TOP_Y = -260
BOTTOM_Y = 260
FOV = 400

IMAGE_NAME = "logo.png"
PICTURE_NAME = "picture5.png"
PICTURE_SIDE_NAME = "picture3.png"

LOGO_PARTICLE_SIZE = 4.5
PICTURE_PARTICLE_SIZE = 1.0
DEPTH_STRENGTH = 40.0

particles = []
logo_targets = []
picture_targets = []
img_logo = None
img_picture = None
img_picture_side = None

state = -2
rotation_y = 0
rotation_x = 0
user_input_str = ""
tree_logo_count = 1500
picture_count = 3000

snap_factor = 0.0
current_view = 0

def setup():
    size(1280, 720)
    background(0)
    rectMode(CENTER)
    global img_logo, img_picture, img_picture_side
    
    try:
        img_logo = loadImage(IMAGE_NAME)
        if img_logo: img_logo.resize(550, 0)
        println("111g")
    except:
        println("Error loading logo.png")
        
    try:
        img_picture = loadImage(PICTURE_NAME)
        if img_picture:
            if img_picture.width > 700: img_picture.resize(700, 0)
    except:
        println("Error loading picture5.png")

    try:
        img_picture_side = loadImage(PICTURE_SIDE_NAME)
        if not img_picture_side and img_picture:
            img_picture_side = img_picture.get()
    except:
        println("Error loading picture_side.png")
    
    textSize(24)
    textAlign(CENTER, CENTER)

def draw():
    global rotation_y, rotation_x, state, snap_factor, current_view
    
    if state < 0:
        background(0)
        fill(255)
        prompt = ""
        if state == -2:
            prompt = "Step 1/2: Enter TREE & LOGO Particle Count\n(Recommended: 5000)"
        elif state == -1:
            prompt = "Step 2/2: Enter PICTURE Particle Count\n(Recommended: 13000)"
        text(prompt, width/2, height/2 - 50)
        
        fill(255, 215, 0)
        textSize(40)
        text(user_input_str + "_", width/2, height/2 + 50)
        textSize(24)
        fill(100)
        text("Press ENTER to confirm", width/2, height/2 + 120)
        return

    fill(2, 2, 5, 200)
    rect(width/2, height/2, width, height)
    
    pushMatrix()
    translate(width/2, height/2)
    
    target_rot_y = 0
    target_rot_x = 0
    
    if state == 1:
        target_rot_y = map(mouseX, 0, width, -PI, PI)
        target_rot_x = map(mouseY, 0, height, -PI/8, PI/8)
        rotation_y = lerp(rotation_y, target_rot_y, 0.05)
        rotation_x = lerp(rotation_x, target_rot_x, 0.05)
        
    elif state == 0:
        mouse_speed = dist(mouseX, mouseY, pmouseX, pmouseY)
        raw_y = map(mouseX, 0, width, -PI/1.5, PI/1.5)
        raw_x = map(mouseY, 0, height, -PI/30, PI/30)
        
        dist_0 = abs(raw_y)
        dist_90 = abs(raw_y - PI/2)
        dist_n90 = abs(raw_y + PI/2)
        
        threshold = 0.25
        target_snap = 0.0
        locked_angle = raw_y
        
        if dist_0 < threshold:
            current_view = 0
            target_snap = map(dist_0, 0, threshold, 1.0, 0.0)
            locked_angle = 0
        elif dist_90 < threshold:
            current_view = 1
            target_snap = map(dist_90, 0, threshold, 1.0, 0.0)
            locked_angle = PI/2
        elif dist_n90 < threshold:
            current_view = 1
            target_snap = map(dist_n90, 0, threshold, 1.0, 0.0)
            locked_angle = -PI/2
        else:
            target_snap = 0.0
            locked_angle = raw_y

        if target_snap > 0.75 and mouse_speed < 2.0:
            target_snap = 1.0

        snap_factor = lerp(snap_factor, target_snap, 0.1)
        
        if snap_factor > 0.5:
            rotation_y = lerp(rotation_y, locked_angle, 0.2)
            rotation_x = lerp(rotation_x, 0, 0.2)
        else:
            rotation_y = lerp(rotation_y, raw_y, 0.1)
            rotation_x = lerp(rotation_x, raw_x, 0.1)

    else:
        rotation_y = lerp(rotation_y, 0, 0.05)
        rotation_x = lerp(rotation_x, 0, 0.05)
    
    cx, sx = cos(rotation_x), sin(rotation_x)
    cy, sy = cos(rotation_y), sin(rotation_y)
    
    blendMode(ADD)
    for p in particles:
        p.update(state, snap_factor, current_view)
        p.draw_optimized(cx, sx, cy, sy, state, snap_factor, current_view)
    blendMode(BLEND)
    popMatrix()
    
    fill(255)
    textAlign(LEFT, TOP)
    textSize(16)
    
    if state == 0:
        info = "Phase 0: Magic Puzzle (Count: " + str(picture_count) + ")"
        text(info, 20, 20)
        bar_w = 200
        noStroke()
        fill(50)
        rect(width/2, height-40, bar_w, 10)
        fill(0, 255, 0)
        rect(width/2, height-40, bar_w * snap_factor, 10)
        
        textAlign(CENTER, BOTTOM)
        if snap_factor > 0.9:
            fill(0, 255, 100)
            textSize(20)
            text("[ PUZZLE SOLVED ]", width/2, height - 60)
        else:
            fill(150)
            textSize(16)
            text("Rotate to combine particles...", width/2, height - 60)
            
    elif state == 1:
        text("Phase 1: Tree (Count: " + str(tree_logo_count) + ")", 20, 20)
    else:
        text("Phase 2: Logo (Count: " + str(tree_logo_count) + ")", 20, 20)

def keyPressed():
    global user_input_str, state, tree_logo_count, picture_count
    if state < 0:
        if key == ENTER or key == RETURN:
            if user_input_str == "": return
            val = int(user_input_str)
            if state == -2:
                tree_logo_count = val
                state = -1
                user_input_str = ""
            elif state == -1:
                picture_count = val
                state = 0
                start_simulation()
        elif key == BACKSPACE:
            if len(user_input_str) > 0:
                user_input_str = user_input_str[:-1]
        elif key >= '0' and key <= '9':
            user_input_str += key

def mousePressed():
    global state
    if state == 0: state = 1
    elif state == 1:
        state = 2
        assign_logo_targets()

def start_simulation():
    total_needed = max(tree_logo_count, picture_count)
    process_puzzle_pixels() 
    process_logo_pixels()
    
    for i in range(total_needed):
        p = GinkgoParticle(i)
        if i < len(picture_targets):
            pt = picture_targets[i]
            p.set_picture_target(
                pt['perfect_vec'], pt['scatter_vec'], 
                pt['col'], pt['size'], pt['type']
            )
        else:
            p.set_picture_target(PVector(0,0,0), PVector(0,0,0), color(0,0), 0, -1)
        particles.append(p)

def process_puzzle_pixels():
    global picture_targets
    picture_targets = []
    
    count_front = int(picture_count * 0.5)
    count_side = picture_count - count_front
    chaos_depth = 1200
    
    if img_picture:
        img_picture.loadPixels()
        aspect = float(img_picture.width) / img_picture.height
        cols = int(sqrt(count_front * aspect))
        rows = int(count_front / cols) if cols > 0 else 1
        dx, dy = float(img_picture.width) / cols, float(img_picture.height) / rows
        p_size = max(dx, dy) * 1.05
        off_x, off_y = -img_picture.width / 2, -img_picture.height / 2
        
        for r in range(rows):
            for c in range(cols):
                px = int(constrain(c * dx, 0, img_picture.width - 1))
                py = int(constrain(r * dy, 0, img_picture.height - 1))
                col = img_picture.pixels[px + py * img_picture.width]
                if alpha(col) < 5: continue
                perfect_pos = PVector(c * dx + off_x, r * dy + off_y, 0)
                scatter_pos = PVector(perfect_pos.x, perfect_pos.y, random(-chaos_depth, chaos_depth))
                picture_targets.append({
                    'perfect_vec': perfect_pos, 'scatter_vec': scatter_pos,
                    'col': col, 'size': p_size, 'type': 0
                })

    if img_picture_side:
        img_picture_side.loadPixels()
        aspect = float(img_picture_side.width) / img_picture_side.height
        cols = int(sqrt(count_side * aspect))
        rows = int(count_side / cols) if cols > 0 else 1
        dx, dy = float(img_picture_side.width) / cols, float(img_picture_side.height) / rows
        p_size = max(dx, dy) * 1.05
        off_x, off_y = -img_picture_side.width / 2, -img_picture_side.height / 2
        
        for r in range(rows):
            for c in range(cols):
                px = int(constrain(c * dx, 0, img_picture_side.width - 1))
                py = int(constrain(r * dy, 0, img_picture_side.height - 1))
                col = img_picture_side.pixels[px + py * img_picture_side.width]
                if alpha(col) < 5: continue
                img_x_mapped_to_z = c * dx + off_x
                perfect_pos = PVector(0, r * dy + off_y, img_x_mapped_to_z)
                scatter_pos = PVector(random(-chaos_depth, chaos_depth), perfect_pos.y, perfect_pos.z)
                picture_targets.append({
                    'perfect_vec': perfect_pos, 'scatter_vec': scatter_pos,
                    'col': col, 'size': p_size, 'type': 1
                })

    import random as rnd
    rnd.shuffle(picture_targets)

def process_logo_pixels():
    global logo_targets
    if not img_logo: return
    img_logo.loadPixels()
    logo_targets = []
    off_x, off_y = -img_logo.width / 2, -img_logo.height / 2
    auto_step = 1.5
    y = 0.0
    while y < img_logo.height:
        x = 0.0
        while x < img_logo.width:
            px, py = int(x), int(y)
            idx = px + py * img_logo.width
            if idx < len(img_logo.pixels):
                c = img_logo.pixels[idx]
                if alpha(c) > 40 and brightness(c) < 240:
                    logo_targets.append({'vec': PVector(px + off_x, py + off_y), 'col': c})
            x += auto_step
        y += auto_step

def assign_logo_targets():
    if not logo_targets: return
    import random as rnd
    rnd.shuffle(logo_targets)
    for i, p in enumerate(particles):
        if i < tree_logo_count:
            t = logo_targets[i % len(logo_targets)]
            p.logo_target, p.logo_col = t['vec'], t['col']
        else:
            p.logo_target = None
#画树

class GinkgoParticle(object):
    def __init__(self, index):
        self.index = index
        self.x, self.y, self.z = 0, 0, 0
        self.current_col = color(255)
        self.current_size = 0
        
        is_trunk = (index % 7 == 0) 
        if is_trunk:

            h_norm = random(0, 1)
            self.treeY = map(h_norm, 0, 1, BOTTOM_Y + 50, TOP_Y * 0.5)
            base_radius = map(h_norm, 0, 1, TREE_WIDTH * 0.15, TREE_WIDTH * 0.06)
            angle = random(TWO_PI)
            radius_noise = noise(h_norm * 5, angle) * 20
            final_radius = base_radius + radius_noise
            curve_x = sin(h_norm * PI) * 20
            self.treeX = cos(angle) * final_radius + curve_x
            self.treeZ = sin(angle) * final_radius
            
            c_noise = noise(h_norm * 10, self.index)
            if c_noise > 0.6: self.tree_col = color(139, 105, 20) 
            elif c_noise > 0.3: self.tree_col = color(101, 67, 33) 
            else: self.tree_col = color(80, 50, 20)  
            self.tree_base_size = random(2.0, 3.5)
        else:

            center_y = TOP_Y * 0.8
            phi, theta = random(0, PI), random(0, TWO_PI) 
            base_r = TREE_WIDTH * 0.9 * pow(random(0.1, 1.0), 0.4)
            bx, by, bz = base_r * sin(phi) * cos(theta), base_r * cos(phi) * 0.8, base_r * sin(phi) * sin(theta)
            n_scale, n_str = 0.007, 180.0
            nx = noise(bx * n_scale + 100, by * n_scale, bz * n_scale)
            ny = noise(bx * n_scale, by * n_scale + 200, bz * n_scale)
            nz = noise(bx * n_scale, by * n_scale, bz * n_scale + 300)
            self.treeX = bx + (nx * 2 - 1) * n_str
            self.treeY = center_y + by + (ny * 2 - 1) * n_str * 0.7
            self.treeZ = bz + (nz * 2 - 1) * n_str

            col_noise = noise(self.treeX * 0.006, self.treeY * 0.006, self.treeZ * 0.006)

            if random(1) < 0.15: 

                self.tree_col = color(100, 160, 45) 
            else:

                if col_noise > 0.75: self.tree_col = color(255, 245, 50)
                elif col_noise > 0.50: self.tree_col = color(255, 215, 0)
                elif col_noise > 0.30: self.tree_col = color(218, 165, 32)
                elif col_noise > 0.15: self.tree_col = color(180, 140, 10)
                else: self.tree_col = color(140, 190, 60) 
            
            self.tree_base_size = random(1.5, 4.5)

        f_angle = random(TWO_PI)
        f_radius = sqrt(random(0, 1)) * 600 # 扩散半径
        self.floorX = cos(f_angle) * f_radius
        self.floorZ = sin(f_angle) * f_radius

        self.floorY = BOTTOM_Y + 50 + (noise(self.floorX * 0.01, self.floorZ * 0.01) * 30)

        f_col_n = noise(self.floorX * 0.005, self.floorZ * 0.005)
        if f_col_n > 0.6: self.floor_col = color(40, 60, 20) # 暗绿
        elif f_col_n > 0.4: self.floor_col = color(80, 70, 20) # 暗金
        else: self.floor_col = color(50, 40, 30) # 泥土
        self.floor_size = random(1.0, 3.0)

        self.pic_perfect = PVector(0,0,0)
        self.pic_scatter = PVector(0,0,0)
        self.pic_col, self.pic_size, self.pic_group = color(0,0), 0, -1
        self.logo_target, self.logo_col = None, color(0,0)

    def set_picture_target(self, perfect, scatter, col, size, group):
        self.pic_perfect, self.pic_scatter = perfect, scatter
        self.pic_col, self.pic_size, self.pic_group = col, size, group
        self.x, self.y, self.z = scatter.x, scatter.y, scatter.z
        self.current_col = col

    def update(self, current_state, snap_val, view_mode):
        target_pos, target_c, target_s = None, None, 0
        
        if current_state == 0:

            if self.pic_group != -1:
                is_my_turn = (self.pic_group == view_mode)
                if is_my_turn:
                    t = snap_val * snap_val * (3 - 2 * snap_val) 
                    tx = lerp(self.pic_scatter.x, self.pic_perfect.x, t)
                    ty = lerp(self.pic_scatter.y, self.pic_perfect.y, t)
                    tz = lerp(self.pic_scatter.z, self.pic_perfect.z, t)
                    target_pos = PVector(tx, ty, tz)
                else:
                    target_pos = self.pic_scatter
                target_c, target_s = self.pic_col, self.pic_size
            else:
                target_s = 0

        elif current_state == 1:

            if self.index < tree_logo_count:
                target_pos = PVector(self.treeX, self.treeY, self.treeZ)
                target_c, target_s = self.tree_col, self.tree_base_size
            else:
                target_pos = PVector(self.floorX, self.floorY, self.floorZ)
                target_c, target_s = self.floor_col, self.floor_size
                
        elif current_state == 2:

            if self.index < tree_logo_count and self.logo_target:
                target_pos = PVector(self.logo_target.x, self.logo_target.y, 0)
                target_c, target_s = self.logo_col, LOGO_PARTICLE_SIZE
            else:
                target_s = 0
#平滑
        if target_pos:
            self.x += (target_pos.x - self.x) * 0.1
            self.y += (target_pos.y - self.y) * 0.1
            self.z += (target_pos.z - self.z) * 0.1
        if target_c:
            self.current_col = lerpColor(self.current_col, target_c, 0.05)
        self.current_size = lerp(self.current_size, target_s, 0.1)

    def draw_optimized(self, cx, sx, cy, sy, state, snap_val, view_mode):
        if self.current_size < 0.1: return
        final_alpha = 255
        
        if state == 0 and self.pic_group != -1:
            if self.pic_group != view_mode:
                final_alpha = constrain(map(snap_val, 0.5, 1.0, 255, 5), 5, 255)
        
        if final_alpha < 10: return

        x1, z1 = self.x * cy - self.z * sy, self.z * cy + self.x * sy
        rx, ry, rz = x1, self.y * cx - z1 * sx, z1 * cx + self.y * sx
        
        val = FOV + rz
        if val > 0:
            scale_f = FOV / val
            s = self.current_size * scale_f
            r, g, b = red(self.current_col), green(self.current_col), blue(self.current_col)
            fill(r, g, b, final_alpha)
            noStroke()
            if state == 0:
                rect(rx * scale_f, ry * scale_f, s * 1.05, s * 1.05)
            else:
                ellipse(rx * scale_f, ry * scale_f, s, s)
