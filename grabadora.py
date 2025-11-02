#!/usr/bin/env python3
import subprocess
import time
import os
import signal
import sys
# Directorio de salida
output_dir = "/home/hera/grabaciones"
os.makedirs(output_dir, exist_ok=True)
# Nombre del archivo
output_file = os.path.join(output_dir, f"grabacion_{time.strftime('%Y%m%d_%H%M%S')}.mp4")
print("Grabador de Pantalla para Hyprland")
print(f"Guardando en: {output_file}\n")
# Detectar herramienta
recorder = None
try:
    subprocess.check_output(['which', 'wf-recorder'], stderr=subprocess.DEVNULL)
    recorder = 'wf-recorder'
    print("Usando wf-recorder")
except:
    pass
if not recorder:
    try:
        subprocess.check_output(['which', 'wl-screenrec'], stderr=subprocess.DEVNULL)
        recorder = 'wl-screenrec'
        print("Usando wl-screenrec")
    except:
        pass
if not recorder:
    print("No se encontro grabador de pantalla para Wayland\n")
    print("Instala una opcion:")
    print("  yay -S wl-screenrec")
    print("  yay -S wf-recorder")
    sys.exit(1)
process = None
try:
    # Configurar comando
    if recorder == 'wl-screenrec':
        cmd = ['wl-screenrec', '--no-hw', '-f', output_file, '--audio', '--audio-device', 'alsa_output.pci-0000_00_1f.3.analog-stereo.monitor']
    else:
        cmd = [
            'wf-recorder', '-f', output_file, '-c', 'libx264',
            '-p', 'preset=ultrafast', '-p', 'crf=23', '-r', '30',
            '--audio=alsa_output.pci-0000_00_1f.3.analog-stereo.monitor'
        ]
    
    print("\nIniciando grabacion en 2 segundos...")
    time.sleep(2)
    
    # Iniciar grabacion
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("GRABANDO... Presiona Ctrl+C para detener\n")
    
    # Manejo de Ctrl+C
    def signal_handler(sig, frame):
        print("\nDeteniendo grabacion...")
        if process:
            process.send_signal(signal.SIGINT)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        time.sleep(1)
        
        # Verificar archivo
        if os.path.exists(output_file):
            print(f"Grabacion guardada: {output_file}")
            
            try:
                # Info del video
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 
                     'format=duration', '-of', 
                     'default=noprint_wrappers=1:nokey=1', output_file],
                    capture_output=True, text=True, timeout=5
                )
                
                if result.stdout.strip():
                    dur = float(result.stdout.strip())
                    print(f"Duracion: {dur:.2f} segundos")
                
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"Tamanio: {size:.2f} MB")
                
                print(f"\nReproducir con: mpv {output_file}")
            except Exception as e:
                print(f"No se pudo obtener info del video: {e}")
        else:
            print("Error: No se pudo crear el archivo")
            if process and process.stderr:
                stderr = process.stderr.read().decode()
                if stderr:
                    print(f"\nError: {stderr[:300]}")
        
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Esperar
    returncode = process.wait()
    
    if returncode != 0:
        stderr = process.stderr.read().decode()
        print(f"\nError en la grabacion:")
        print(stderr[:500])
        print("\nPosibles causas:")
        print("- Otra grabacion ya activa")
        print("- Compositor no responde")
        print("- Permisos insuficientes")
except KeyboardInterrupt:
    signal_handler(None, None)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if process:
        try:
            process.terminate()
        except:
            pass
