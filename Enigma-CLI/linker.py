#!/usr/bin/env python3
import os
import sys

def create_relative_link(target, link_name):
    target_path = os.path.abspath(target)
    link_dir = os.path.dirname(link_name)
    relative_path = os.path.relpath(target_path, link_dir)
    os.symlink(relative_path, link_name)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: linker.py <caminho_para_alvo> <caminho_para_atalho>")
        sys.exit(1)

    target = sys.argv[1]
    link_name = sys.argv[2]

    create_relative_link(target, link_name)

