"""Project Atlas-style faceted geometry into native SVG/SMIL, without raster frames.

Lighting and the two-layer color model follow the original Atlas core; SVG uses
one flat color per triangle instead of WebGL's per-pixel shader. Standard-library
only, so `python scripts/profile.py design` rebuilds the entire header.
"""
from math import cos, floor, pi, sin, sqrt, tan


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def normalized(v):
    length = sqrt(dot(v, v))
    return tuple(x / length for x in v)


def mix(a, b, t):
    return a * (1 - t) + b * t


def smooth(a, b, value):
    t = max(0, min(1, (value - a) / (b - a)))
    return t * t * (3 - 2 * t)


def noise(p):
    base = [floor(v) for v in p]
    f = [smooth(0, 1, v - floor(v)) for v in p]

    def hashed(x, y, z):
        value = sin(dot((base[0]+x, base[1]+y, base[2]+z), (127.1, 311.7, 74.7))) * 43758.5453123
        return value - floor(value)

    planes = []
    for z in (0, 1):
        planes.append(mix(mix(hashed(0, 0, z), hashed(1, 0, z), f[0]),
                          mix(hashed(0, 1, z), hashed(1, 1, z), f[0]), f[1]))
    return mix(*planes, f[2])


def turbulence(p):
    result, amplitude = 0, .52
    for _ in range(5):
        result += noise(p) * amplitude
        p = tuple(v * 2.03 + 7.1 for v in p)
        amplitude *= .5
    return result


def geometry():
    """The same 20-face icosahedron and detail-4 subdivision as the Atlas mesh."""
    t = (1 + sqrt(5)) / 2
    vertices = [(-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),(0,-1,t),(0,1,t),
                (0,-1,-t),(0,1,-t),(t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1)]
    indices = [(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),
               (5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),
               (3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),
               (8,6,7),(9,8,1)]
    divisions = 5
    triangles = []
    for indices_face in indices:
        a, b, c = [vertices[i] for i in indices_face]

        def point(i, j):
            return normalized(tuple((a[k]*(divisions-i-j) + b[k]*i + c[k]*j) / divisions for k in range(3)))

        for i in range(divisions):
            for j in range(divisions-i):
                triangles.append((point(i,j), point(i+1,j), point(i,j+1)))
                if i+j < divisions-1:
                    triangles.append((point(i+1,j), point(i+1,j+1), point(i,j+1)))
    return triangles


LIGHT = normalized((.28, .52, .81))
CAMERA = (0, .12, 6.7)


def shade(normal, center, pattern):
    """Composite the red core and reflective shell under Atlas's fixed light."""
    d = max(0, dot(normal, LIGHT))
    m = smooth(.46, .92, d) ** 2.6
    e = pattern
    inner = [mix(mix(a,b,d**.8),c,m*(.38+e*.62))
             for a,b,c in zip((.008,.009,.012),(.038,.027,.032),(.42,.002,.005))]
    inner = [v + c*m*(.2+e*.48)*(.42+d**3*1.45)
             for v,c in zip(inner,(1,.018,.011))]
    f, specular, bright = smooth(.46,.92,d)**1.15, d**68*m, d**7*m
    highlight = smooth(.9817,.9925,d)
    view = normalized(tuple(CAMERA[k]-center[k]*1.9 for k in range(3)))
    rim = (1-max(0,dot(normal,view)))**3.5
    outer = [mix(a,b,d**.72)+c*f*(.12+d*.55)+s*specular*3.2+r*bright+n*d*d*.38*(1-m)+edge*rim*.22
             for a,b,c,s,r,n,edge in zip((.012,.014,.018),(.05,.054,.062),(.46,.42,.4),
                                       (1,.94,.9),(.58,.035,.038),(.16,.17,.19),(.07,.01,.014))]
    outer = [mix(v,c,highlight) for v,c in zip(outer,(1.65,1.48,1.3))]
    alpha = mix(max(.16,min(.88,mix(.82,.05,m)+specular*.16)),.80,highlight)

    def display(v):
        # Atlas's custom ShaderMaterial writes its own final fragment color.
        return round(255 * max(0, min(1, v)))

    return '#' + ''.join(f'{display(mix(a,b,alpha)):02x}' for a,b in zip(inner,outer))


def render_sphere(animated=True):
    count = 48 if animated else 1
    faces = []
    camera_distance = sqrt(dot(CAMERA,CAMERA))
    up_y, up_z = CAMERA[2]/camera_distance, -CAMERA[1]/camera_distance
    focal = 110 / tan(17*pi/180)
    for triangle in geometry():
        original_center = tuple(sum(p[k] for p in triangle)/3 for k in range(3))
        sample = tuple(v*5.3 for v in normalized(original_center))
        a, b = turbulence(sample), turbulence(tuple(v*2.4 for v in sample))
        pattern = smooth(.43,.82,a+b*.3+sin(b*2*pi)*.025)
        paths, colors, visibility = [], [], []
        for frame in range(count):
            angle = -frame/count*2*pi

            def rotate(p):
                return (p[0]*cos(angle)+p[2]*sin(angle),p[1],-p[0]*sin(angle)+p[2]*cos(angle))

            points = [rotate(p) for p in triangle]
            center = rotate(original_center)
            u = tuple(points[1][k]-points[0][k] for k in range(3))
            v = tuple(points[2][k]-points[0][k] for k in range(3))
            normal = normalized((u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]))
            if dot(normal,center) < 0:
                normal = tuple(-v for v in normal)
            visible = dot(normal,tuple(CAMERA[k]-center[k]*1.9 for k in range(3))) > 0
            projected = []
            for x,y,z in points:
                depth = camera_distance-1.9*(y*CAMERA[1]+z*CAMERA[2])/camera_distance
                projected.append((682+focal*x*1.9/depth,158-focal*(y*up_y+z*up_z)*1.9/depth))
            paths.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in projected)+'Z')
            colors.append(shade(normal,center,pattern))
            visibility.append('1' if visible else '0')
        motion = ''
        if animated:
            for attribute, values, mode in [('d',paths,'linear'),('fill',colors,'linear'),('opacity',visibility,'discrete')]:
                motion += f'<animate attributeName="{attribute}" values="{";".join(values+[values[0]])}" dur="18s" repeatCount="indefinite" calcMode="{mode}"/>'
        if animated or visibility[0] == '1':
            faces.append(f'<path d="{paths[0]}" fill="{colors[0]}" opacity="{visibility[0]}">{motion}</path>')
    return ('<g aria-label="Rotating faceted Atlas sphere">'
            '<circle cx="682" cy="158" r="108" fill="#09090D" stroke="#a90b11" stroke-width="2"/>'
            '<circle cx="682" cy="158" r="106.8" fill="#09090D" stroke="#fff5e8" stroke-width="1"/>'
            + ''.join(faces) + '</g>')
