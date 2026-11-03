"""Format new story dialogue for two-row HeartGold message pages."""
import re,textwrap

def format_dialogue(text,width=32):
    text=text.replace("'",'’').replace('Pokemon','Pokémon').replace('Poke Balls','Poké Balls')
    pages=[]
    for page in text.split('\r'):
        variables={}
        def protect(match):
            token=f'@{len(variables):05}@';variables[token]=match.group();return token
        page=re.sub(r'\{[^}]+\}',protect,page)
        lines=textwrap.wrap(page.replace('\n',' '),width=width,break_long_words=False,break_on_hyphens=False)
        for start in range(0,len(lines),2):
            value='\n'.join(lines[start:start+2])
            for token,var in variables.items():value=value.replace(token,var)
            pages.append(value)
    return '\r'.join(pages)
