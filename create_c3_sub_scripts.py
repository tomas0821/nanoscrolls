import os

template_path = 'binding_energy/run_c1_v73.sh'
with open(template_path, 'r') as f:
    template = f.read()

subconfigs = ['c3_rot90', 'c3_flip', 'c3_shift', 'c3_diag']

for name in subconfigs:
    new_script = template.replace('CNS_c1_v73', f'CNS_{name}')
    new_script = new_script.replace('c1_v73.out', f'{name}.out')
    new_script = new_script.replace('c1_v73.err', f'{name}.err')
    new_script = new_script.replace('c1/out', f'{name}/out')
    new_script = new_script.replace('cd c1', f'cd {name}')
    new_script = new_script.replace('Starting c1', f'Starting {name}')
    new_script = new_script.replace('Finished c1', f'Finished {name}')
    
    script_path = f'binding_energy/run_{name}.sh'
    with open(script_path, 'w') as f:
        f.write(new_script)
    print(f"Created {script_path}")
