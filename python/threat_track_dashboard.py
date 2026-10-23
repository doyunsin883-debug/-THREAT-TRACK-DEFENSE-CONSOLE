"""THREAT-TRACK tactical-styled proximity telemetry viewer.

Works with the Arduino sketch supplied in this repository.
Run `python threat_track_dashboard.py --port COM5` or `--demo` to preview without hardware.
The radar sweep is decorative; a single HC-SR04 only measures forward range.
"""
import argparse
import math
import queue
import random
import threading
import time
import tkinter as tk
from collections import deque
from datetime import datetime
from telemetry import parse_packet, Telemetry

BG = '#08131B'
PANEL = '#0D202A'
EDGE = '#1C4551'
GREEN = '#35E5A7'
MUTED = '#789B9D'
TEXT = '#D7F6E7'
RED = '#FF6477'
YELLOW = '#FAD16B'

parser = argparse.ArgumentParser(description='THREAT-TRACK Tactical Console')
parser.add_argument('--port', default='COM5', help='Serial port, default COM5')
parser.add_argument('--baud', type=int, default=9600)
parser.add_argument('--demo', action='store_true', help='Use labeled simulated data instead of a real sensor')
parser.add_argument('--list-ports', action='store_true', help='Show available serial ports and exit')
args = parser.parse_args()

if args.list_ports:
    try:
        from serial.tools import list_ports
        ports = list(list_ports.comports())
        print('\n'.join(f'{p.device} – {p.description}' for p in ports) if ports else 'No serial ports detected')
    except ImportError:
        print('Install dependency: py -m pip install -r requirements.txt')
    raise SystemExit(0)

messages: queue.Queue = queue.Queue()
stop = threading.Event()


def serial_worker():
    try:
        import serial
        with serial.Serial(args.port, args.baud, timeout=0.5) as conn:
            messages.put(('connection', f'CONNECTED {args.port}'))
            while not stop.is_set():
                text = conn.readline().decode('utf-8', errors='ignore').strip()
                if not text:
                    continue
                try:
                    packet = parse_packet(text)
                except ValueError:
                    messages.put(('invalid', text[:90]))
                    continue
                messages.put(('telemetry', packet))
    except ImportError:
        messages.put(('error', 'pyserial missing. Run: py -m pip install -r requirements.txt'))
    except Exception as e:
        messages.put(('error', f'COM PORT ERROR: {e}'))

class Console:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('THREAT-TRACK | Tactical Proximity Console')
        self.root.geometry('1240x810')
        self.root.minsize(1080, 710)
        self.root.configure(bg=BG)
        self.last_packet: Telemetry | None = None
        self.last_seen = 0.0
        self.connection = 'SIMULATION / DEMO MODE' if args.demo else 'CONNECTING ...'
        self.history = deque(maxlen=90)
        self.last_status = ''
        self.demo_start = time.monotonic()
        self.demo_next = 0.0
        self.build()
        if not args.demo:
            threading.Thread(target=serial_worker, daemon=True).start()
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.update()
        self.root.mainloop()

    def build(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill='x', padx=30, pady=(21, 6))
        tk.Label(header, text='THREAT—TRACK', fg=GREEN, bg=BG, font=('Consolas', 30, 'bold')).pack(side='left')
        tk.Label(header, text='TACTICAL PROXIMITY MONITOR  /  V5.0', fg=MUTED, bg=BG, font=('Consolas', 12)).pack(side='right', pady=17)
        tk.Frame(self.root, bg=EDGE, height=2).pack(fill='x', padx=30)
        self.status_line = tk.Label(self.root, fg=MUTED, bg=BG, anchor='w', font=('Consolas', 12))
        self.status_line.pack(fill='x', padx=30, pady=(12, 14))
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill='both', expand=True, padx=30)
        left = tk.Frame(body, bg=PANEL, highlightbackground=EDGE, highlightthickness=1)
        left.pack(side='left', fill='both', expand=True, padx=(0, 12))
        right = tk.Frame(body, bg=BG, width=410)
        right.pack(side='right', fill='y')
        right.pack_propagate(False)
        tk.Label(left, text='FORWARD RANGE / 단일 정면 거리', fg=GREEN, bg=PANEL, font=('Consolas', 15, 'bold')).pack(anchor='w', padx=21, pady=(18, 5))
        self.radar = tk.Canvas(left, bg=PANEL, highlightthickness=0, height=510)
        self.radar.pack(fill='both', expand=True, padx=18)
        tk.Label(left, text='DECORATIVE SWEEP ONLY   •   NOT A 360° RADAR   •   SENSOR AXIS = 0°', fg=MUTED, bg=PANEL, font=('Consolas', 10)).pack(pady=(2, 22))
        self.readouts = {}
        for key, desc in [('DISTANCE', '거리 / cm'), ('APPROACH SPEED', '접근 속도 / cm/s'), ('EST. CONTACT TIME', '예상 접촉 시간 / s'), ('ALERT STATE', '위험도')]:
            frame = tk.Frame(right, bg=PANEL, highlightthickness=1, highlightbackground=EDGE)
            frame.pack(fill='x', pady=(0, 10))
            tk.Label(frame, text=f'{key}  /  {desc}', fg=MUTED, bg=PANEL, font=('Consolas', 10)).pack(anchor='w', padx=18, pady=(10, 2))
            v=tk.Label(frame, text='—', fg=TEXT, bg=PANEL, font=('Consolas', 25, 'bold'))
            v.pack(anchor='w', padx=18, pady=(0, 10))
            self.readouts[key]=v
        tk.Label(right, text='RANGE HISTORY  /  거리 추이', fg=GREEN, bg=BG, font=('Consolas', 11, 'bold')).pack(anchor='w', pady=(8, 0))
        self.graph=tk.Canvas(right,bg=PANEL,height=112,highlightthickness=1,highlightbackground=EDGE)
        self.graph.pack(fill='x',pady=(6,12))
        tk.Label(right,text='EVENT LOG / 이벤트 로그',fg=GREEN,bg=BG,font=('Consolas',11,'bold')).pack(anchor='w')
        self.log=tk.Text(right,width=47,height=7,bg=PANEL,fg=GREEN,font=('Consolas',10),relief='flat',state='disabled')
        self.log.pack(fill='both',expand=True,pady=(6,0))
        foot=tk.Label(self.root,text='PROTOTYPE · ULTRASONIC RANGE SENSOR · NOT A MILITARY-GRADE RADAR OR SAFETY DEVICE',fg=MUTED,bg=BG,font=('Consolas',10))
        foot.pack(pady=(13,18))

    def event(self,msg):
        self.log.configure(state='normal')
        self.log.insert('end', f'[{datetime.now():%H:%M:%S}]  {msg}\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def sample_demo(self):
        t=time.monotonic()-self.demo_start
        # In a deliberately labeled demo, oscillate approach and retreat.
        d=94 - 64 * math.sin(t/3.4)
        speed=(64/3.4) * math.cos(t/3.4)
        ttc=d/speed if speed > 10 else None
        state='DANGER' if d <=30 or (ttc is not None and ttc <=1.5) else 'WARNING' if d<=70 or (ttc is not None and ttc<=3.0) else 'SAFE'
        return Telemetry(d,speed,ttc,state)

    def receive(self,packet):
        self.last_packet=packet
        self.last_seen=time.monotonic()
        if packet:
            self.history.append(packet.distance_cm)
            if packet.status!=self.last_status:
                self.event('ALERT → '+packet.status)
                self.last_status=packet.status
        elif self.last_status!='NO SIGNAL':
            self.event('NO VALID ULTRASONIC SIGNAL')
            self.last_status='NO SIGNAL'

    def render(self):
        packet=self.last_packet
        stale=(not args.demo) and (time.monotonic()-self.last_seen > 2.5)
        connected=not stale and packet is not None
        if stale:
            self.status_line.config(text=f'LINK: {self.connection}  |  DATA: STALE / WAITING',fg=YELLOW)
        else:
            self.status_line.config(text=f'LINK: {self.connection}  |  MODE: {"SIMULATED" if args.demo else "LIVE SERIAL"}',fg=GREEN)
        keys=self.readouts
        keys['DISTANCE'].config(text=f'{packet.distance_cm:06.1f}' if connected else '—')
        keys['APPROACH SPEED'].config(text=f'{packet.approach_cm_s:+06.1f}' if connected else '—')
        keys['EST. CONTACT TIME'].config(text=f'{packet.ttc_s:05.2f}' if connected and packet.ttc_s is not None else 'N/A')
        status=packet.status if connected else 'NO SIGNAL'
        color={'SAFE':GREEN,'WARNING':YELLOW,'DANGER':RED}.get(status,MUTED)
        keys['ALERT STATE'].config(text=status, fg=color)
        self.draw_radar(packet if connected else None,color)
        self.draw_history()

    def draw_radar(self,packet,col):
        c=self.radar;c.delete('all')
        width=max(c.winfo_width(),540)
        height=max(c.winfo_height(),460)
        cx=width/2;cy=height-38;radius=min(width*0.44,height*0.74)
        for frac in [.25,.5,.75,1.0]:
            r=radius*frac
            c.create_arc(cx-r,cy-r,cx+r,cy+r,start=0,extent=180,style='arc',outline=EDGE,width=2)
            c.create_text(cx+r-12,cy-12,text=str(int(frac*150)),fill=MUTED,font=('Consolas',9))
        for deg in [0,30,60,90,120,150,180]:
            phi=math.radians(deg)
            x=cx+radius*math.cos(phi);y=cy-radius*math.sin(phi)
            c.create_line(cx,cy,x,y,fill=EDGE,width=1)
        phi=(time.monotonic()*1.0)%math.pi
        c.create_line(cx,cy,cx+radius*math.cos(phi),cy-radius*math.sin(phi),fill='#176A50',width=4)
        c.create_line(cx,cy,cx,cy-radius,fill=GREEN,dash=(5,5),width=2)
        c.create_text(cx,cy+12,text='HC-SR04 / 0°',fill=GREEN,font=('Consolas',11))
        if packet:
            r=radius*min(packet.distance_cm,150)/150
            tx=cx;ty=cy-r
            c.create_oval(tx-13,ty-13,tx+13,ty+13,outline=col,width=3)
            c.create_oval(tx-4,ty-4,tx+4,ty+4,fill=col,outline=col)
            c.create_text(tx+84,ty-18,text=f'{packet.distance_cm:.1f} cm',fill=col,font=('Consolas',14,'bold'))

    def draw_history(self):
        c=self.graph;c.delete('all')
        w=max(c.winfo_width(),390);h=max(c.winfo_height(),110)
        for i in range(1,4):c.create_line(0,i*h/4,w,i*h/4,fill=EDGE)
        data=list(self.history)
        if len(data)<2:return
        pts=[(20+i*(w-35)/(len(data)-1),h-11-min(d,150)/150*(h-21)) for i,d in enumerate(data)]
        c.create_line(*[v for p in pts for v in p],fill=GREEN,width=2,smooth=False)

    def update(self):
        try:
            while True:
                typ,value=messages.get_nowait()
                if typ=='connection':
                    self.connection=value
                    self.event('SERIAL '+value)
                elif typ=='telemetry':
                    self.receive(value)
                elif typ=='error':
                    self.connection='DISCONNECTED'
                    self.event(str(value))
                elif typ=='invalid':
                    self.event('IGNORED INVALID PACKET: '+str(value)[:70])
        except queue.Empty:
            pass
        if args.demo and time.monotonic()>self.demo_next:
            self.receive(self.sample_demo())
            self.demo_next=time.monotonic()+0.18
        self.render()
        self.root.after(80,self.update)

    def close(self):
        stop.set()
        self.root.destroy()

if __name__=='__main__':
    Console()
