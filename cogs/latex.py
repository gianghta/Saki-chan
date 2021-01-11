import discord
from discord.ext import commands

import aiohttp
import io

TEX_API = 'http://rtex.probablyaweb.site/api/v2'
TEMPLATE = r'''
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{geometry}
\usepackage{mathtools}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{chemfig}
\usepackage{color}
\usepackage{xcolor}
\geometry{textwidth=8cm}
\begin{document}
\pagenumbering{gobble}
\definecolor{darktheme}{HTML}{36393F}
\color{white}
\pagecolor{darktheme}
USERINPUTHERE
\end{document}
'''


class TexRenderError(commands.CommandError):
    def __init__(self, logs):
        self.logs = logs


class LatexCog(commands.Cog, name='Math'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=['tex'],
        help="Generate Latex image from Latex code: saki tex|latex <input code>",
        brief="Generate Latex image from chat input"
    )
    async def latex(self, ctx, *, latex):
        if latex.startswith('```') and latex.endswith('```'):
            latex = '\n'.join(latex.replace('```', '').split('\n'))
        to_render = TEMPLATE.replace('USERINPUTHERE', latex)
        await self.render(ctx, to_render)

    async def render(self, ctx, latex):
        try:
            payload = {'code': latex, 'format': 'png'}
            async with self.bot.session.post(TEX_API, data=payload) as r:
                r.raise_for_status()
                jdata = await r.json()
                if jdata['status'] != 'success':
                    raise TexRenderError(jdata.get('log'))
                file_url = TEX_API + '/' + jdata['filename']

            async with self.bot.session.get(file_url) as fr:
                fr.raise_for_status()
                data = io.BytesIO(await fr.read())
                await ctx.send(file=discord.File(data, 'latex.png'))

        except aiohttp.client_exceptions.ClientResponseError:
            raise TexRenderError(None)


def setup(bot):
    bot.add_cog(LatexCog(bot))