import argparse
from .deploy import deploy

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--target', required=True, choices=['prod', 'test', 'train'])

    args = parser.parse_args()

    deploy(args)
