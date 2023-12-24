import os

thisdir = os.path.dirname(__file__)

def convert2wav(input_file, output_dir = 'WavOutput'):
    assert os.path.exists(input_file), f"No such file or directory: '{input_file}'"
    if not os.path.exists(output_dir):
        os.system(f'mkdir {output_dir}')
    import subprocess
    command = ["ffmpeg", "-loglevel", "fatal", "-i", os.path.join(input_file), "-acodec", "pcm_s16le", "-ac", "1", os.path.join(output_dir, input_file[:-4] + '.wav')]
    subprocess.run(command)
    return os.path.join(output_dir, input_file[:-4] + '.wav')

def _mk_wav_output_dir(output_dir = 'WavOutput'):
    if not os.path.exists(
        os.path.join(thisdir, output_dir)
    ):
        os.system(f"mkdir {os.path.join(thisdir, output_dir)}")
    
    if not os.path.exists(
        os.path.join(thisdir, output_dir, 'Chinese')
    ):
        os.system(f"mkdir {os.path.join(thisdir, output_dir, 'Chinese')}")

    if not os.path.exists(
        os.path.join(thisdir, output_dir, 'Windows')
    ):
        os.system(f"mkdir {os.path.join(thisdir, output_dir, 'Windows')}")

def _clear_wav_output(output_dir = 'WavOutput'):
    os.system(f"rm -r {os.path.join(thisdir, output_dir)}")
    _mk_wav_output_dir(output_dir)
