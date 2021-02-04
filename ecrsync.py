import boto3
import subprocess
from subprocess import PIPE
import json


def pull_images(image_name, registry_url, image_tag):
    command = ['docker', 'pull', registry_url + ':'+image_tag]
    res, st = run_command(command)


def get_image_id(registry_url, image_tag):
    command = ['docker', 'images', registry_url +
               ":" + image_tag, '--quiet']
    res, st = run_command(command)
    if not st:
        print(res)
    return res


def tag_image(image_id, image_tag):
    command = ['docker', 'tag', image_id, image_tag]
    res, st = run_command(command)
    print(res)


def push_images(image_name, registry_url, image_tag):
    command = ['docker', 'push', registry_url+':'+image_tag]
    res, st = run_command(command)
    print(res)


def run_command(command):
    debugcommand = "run {0}".format(" ".join(command))
    print(debugcommand)
    popen = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    popen.wait(500)  # wait a little for docker to complete
    out, err = popen.communicate()
    out = out.decode("utf-8").replace("\n", "")
    err = err.decode("utf-8").replace("\n", "")
    if popen.returncode == 0:
        print("Succeed to run command " + "{0}".format(" ".join(command)))
        return out, True
    else:
        print("Failed to run command " +
              "{0}".format(" ".join(command)))
        exit(2)
        return err, False


def run():
    with open("config.json") as config_file:
        cfg = json.load(config_file)

    image_name = cfg['image_name']
    external_registry_url = cfg['external_registry_url']
    internal_registry_url = cfg['internal_registry_url']
    image_tags = cfg['image_tags']
    for image_tag in image_tags:
        pull_images(image_name, external_registry_url, image_tag)
        image_id = get_image_id(external_registry_url, image_tag)
        print(image_id)
        tag_image(image_id, internal_registry_url+":"+image_tag)
        push_images(image_name, internal_registry_url, image_tag)


if __name__ == "__main__":
    run()
