# prototypo-grabadora
un prototipo de grabadora de pantalla muy simple pero funcional para terminal
para empezar a usar esta herramienta necesitaras un par de dependencias antes de poder usarlo porque usa un par de librerias
esta herramienta esta desarrollada en hyprland aunque deberia funcionar en cualquier DE que sea wayland aun no testeado en x11(tampoco planeo hacerlo)

#arch

sudo pacman -S wf-recorder ffmpeg python mpv

debian based

sudo apt update

sudo apt install wf-recorder ffmpeg python3 mpv

#fedora besed

sudo dnf install ffmpeg python3 mpv

sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm

sudo dnf install wf-recorder ffmpeg python3 mpv
