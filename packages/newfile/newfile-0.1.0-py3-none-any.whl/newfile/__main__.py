import sys
import re
import argparse
from datetime import datetime

import yaml
import click

import jinja2
from jinja2 import Environment, FunctionLoader, select_autoescape


try:
    from rich.console import Console
    from rich.traceback import install
    console = Console()
    install(show_locals=True,suppress=[jinja2,click])
except:
    pass


def load_template(name):
    if not name:
        return ""
    source = ''
    with open(f'newfile_templates/{name}.jinja') as f:
        source = f.read()
    defs = {}
    if re.match(r'\s*===+\n',source):
        s = re.split('\n===+\n',source.lstrip(" =\t\r\n"),1)
        source = s[1]
        pre_param_defs(s[0])

    return source

### init jinja ### 
tlenv = Environment(
loader = FunctionLoader(load_template),
autoescape = select_autoescape(),
undefined=jinja2.DebugUndefined,
finalize=lambda s: s not in [None,False] and s or ''
)
tlctx = {
    'params':[],
    'opts':{},
}
# -- init jinja --

def pre_param_defs(text):
    parser = tlctx['parser']
    ps = yaml.load(text)
    for l,r in ps.items():
        a = []
        k = argparse.Namespace()
        l = l.split(',')
        for i in l:
            i = i.strip()
            if len(i) == 0:
                continue
            if i[0] == '-':
                a.append(i)
            else:
                k.help = i
        t = type(r)
        if t in [int,float]:
            k.type = int
        elif t == list:
            k.type = str
            k.action = 'append'

        elif r == False:
            k.action = 'store_true'
        elif r == True:
            k.action = 'store_false'
        else:
            k.type = str

        k.default = r


        try:
            parser.add_argument(*a,**vars(k))
        except argparse.ArgumentError as e:
            pass
    

def post_args(args,opts):
    param = []
    for arg in args:
        if arg and arg[0] == '-':
            a = arg.split('=',1)
            k = a[0].lstrip('-').replace('-','_')
            if len(a) == 2:
                opts[k] = a[1]
            else:
                opts[k] = True
        else:
            param.append(arg)
    
    return param


def pull_args():
    parser :argparse.ArgumentParser = tlctx['parser']
    (opts,args) = parser.parse_known_args(tlctx['argv'])
    opts = vars(opts)
    params = post_args(args,opts)
    tlctx['params'] = params
    tlctx['opts'] = opts

    for i in tlctx['opts']:
        s = tlctx['opts'][i]
        if type(s) == str and '{{' in s:
            tlctx['opts'][i] = inline_render(s)
        tlenv.globals[i] = tlctx['opts'][i]


def inline_render(text):
    tl = tlenv.from_string(text)
    return tl.render()
    

@click.command(context_settings={
#'ignore_unknown_options':True,
'allow_interspersed_args':False,
'allow_extra_args':True
})
@click.option('-o','--output',is_flag=True,help='output filename or base dir')
@click.argument('template')
@click.argument('args',nargs=-1)
def main(template,args,**opts):
    global tlhandle
    tlenv.globals['_tl_'] = tlctx
    tlenv.globals['now'] = datetime.now().ctime()
    tlargparser = argparse.ArgumentParser(
        prog=template,
        add_help=False
    )
    tlargparser.add_argument('--help','-h','-?',action='store_true', help='display help of template')
    tlctx['parser'] = tlargparser
    tlctx['argv'] = args
    
    tlhandle = tlenv.get_template(template)
    tlargparser.parse_known_args(args)

    tlhandle.render()
    pull_args()
    if tlctx['opts']['help']:
        parser.print_help()
        return

    out = tlhandle.render()
    
    output_file = opts['output'] or template
    with open(output_file,'x') as f:
        f.write(out)
    
    
    
    
if '__main__' == __name__:
    main()
