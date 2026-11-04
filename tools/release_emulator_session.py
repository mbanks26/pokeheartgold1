"""Small JSON control client for reproducible, isolated native-input QA."""
from pathlib import Path
import atexit,json,os,subprocess,sys


class EmulatorSession:
    def __init__(self, core, rom, symbols, output, label='emulator'):
        self.output=Path(output);self.output.mkdir(parents=True,exist_ok=True)
        self.proc=subprocess.Popen([sys.executable,'-u',str(Path(__file__).with_name('companion_emulator_runner.py')),
            '--core',str(core),'--rom',str(rom),'--symbols',str(symbols),'--output',str(self.output)],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        self.log=(self.output/(label+'.stdout.log')).open('x')
        atexit.register(self.abort)
        self.response(ready=True)

    def response(self, ready=False):
        while True:
            line=self.proc.stdout.readline()
            if not line:raise RuntimeError('Emulator exited unexpectedly: '+str(self.proc.poll()))
            self.log.write(line);self.log.flush()
            try:result=json.loads(line)
            except json.JSONDecodeError:continue
            if 'failed' in result:raise AssertionError(result['failed'])
            if (ready and result.get('ready')) or (not ready and 'frame' in result):return result

    def send(self, command):
        self.proc.stdin.write(json.dumps(command)+'\n');self.proc.stdin.flush()
        return self.response()

    def boot_continue(self):
        for command in [{'frames':600},{'frames':3,'buttons':['A']},{'frames':180},
                        {'frames':3,'buttons':['A']},{'frames':300},
                        {'frames':8,'buttons':['A']},{'frames':600}]:self.send(command)
        result=self.send({'frames':1,'inspect':True})
        assert 'flag_address' in result['game'],'Continue did not load a native field save'
        return result

    def save(self):
        for command in [{'frames':8,'buttons':['X']},{'frames':180},
                {'frames':2,'touch':[128,74]},{'frames':360},
                {'frames':8,'buttons':['A']},{'frames':360},
                {'frames':8,'buttons':['A']},{'frames':2400},
                {'frames':8,'buttons':['B']},{'frames':180},
                {'frames':8,'buttons':['B']},{'frames':180}]:self.send(command)

    def close(self):
        self.send({'exit':True});self.proc.wait(timeout=30);self.log.close()
        assert self.proc.returncode==0

    def abort(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:self.proc.kill();self.proc.wait(timeout=10)


def isolated_rom(immutable_rom, output):
    """Link a protected ROM snapshot into a new test folder with its own battery.

    Never pass a mutable build target here: rebuilds must not alter test snapshots.
    The frontend resolves symlinks, so a symlink would share the source battery.
    """
    folder=Path(output);folder.mkdir(parents=True,exist_ok=True)
    target=folder/'test.nds'
    if target.exists() or target.with_suffix('.dsv').exists():raise FileExistsError(target)
    os.link(immutable_rom,target)
    return target
