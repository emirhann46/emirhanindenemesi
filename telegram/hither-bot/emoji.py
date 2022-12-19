import roles
def get_emoji(claim):
    clm = claim.split(" ", 1)
    claimed = clm[0]
    if claimed.lower() in roles.vg:
        return "👱 " 
    elif claimed.lower() in roles.drunk:
        return "🍻 " 
    elif claimed.lower() in roles.seer:
        return "👳 " 
    elif claimed.lower() in roles.harlot:
        return "💋 " 
    elif claimed.lower() in roles.bh:
        return "👁 " 
    elif claimed.lower() in roles.gunner:
        return "🔫 " 
    elif claimed.lower() in roles.ga:
        return "👼 " 
    elif claimed.lower() in roles.fool:
        return "🃏 " 
    elif claimed.lower() in roles.mason or claim.lower() == "lone mason":
        return "👷 " 
    elif claimed.lower() in roles.dete:
        return "🕵️ " 
    elif claimed.lower() in roles.apps:
        return "🙇 " 
    elif claimed.lower() in roles.ch or claim.lower() == "cultist hunter":
        return "💂 " 
    elif claimed.lower() in roles.cupid:
        return "🏹 " 
    elif claimed.lower() in roles.th or claim.lower() == "town hunter":
        return "🎯 " 
    elif claimed.lower() in roles.cg:
        return "🤕 " 
    elif claimed.lower() in roles.bs:
        return "⚒ "  
    elif claimed.lower() in roles.prince:
        return "💍 " 
    elif claimed.lower() in roles.mayor:
        return "🎖 " 
    elif claimed.lower() in roles.oracle:
        return "🌀 " 
    elif claimed.lower() in roles.monarch:
        return "👑 " 
    elif claimed.lower() in roles.paci:
        return "☮️ " 
    elif claimed.lower() in roles.we:
        return "📚 " 
    elif claimed.lower() in roles.sm:
        return "💤 " 
    elif claimed.lower() in roles.wolfman:
        return "👱‍🌚 " 
    elif claimed.lower() in roles.martyr:
        return "🔰 " 
    elif claimed.lower() in roles.alche:
        return "🍵 " 
    elif claimed.lower() in roles.squire:
        return "🛡 " 
    elif claimed.lower() in roles.beauty:
        return "💅 " 
    elif claimed.lower() in roles.sb:
        return "🌩 " 
    elif claimed.lower() in roles.traitor:
        return "🖕 " 
    elif claimed.lower() in roles.wc:
        return "👶 " 
    elif claimed.lower() in roles.cursed:
        return "😾 " 
    elif claimed.lower() in roles.wolfcub or claim.lower() == "wuff cub" or claim.lower () == "wolf cub":
        return "🐶 " 
    elif claimed.lower() in roles.ww:
        return "🐺 " 
    elif claimed.lower() in roles.sorc:
        return "🔮 " 
    elif claimed.lower() in roles.alpha:
        return "⚡️ " 
    elif claimed.lower() in roles.lycan:
        return "🐺🌝 " 
    elif claimed.lower() in roles.prowl:
        return "🦉 " 
    elif claimed.lower() in roles.mystic:
        return "☄️ " 
    elif claimed.lower() in roles.trickster:
        return "🐑 " 
    elif claimed.lower() in roles.fa:
        return "👼🐺 " 
    elif claimed.lower() in roles.arso:
        return "🔥 " 
    elif claimed.lower() in roles.tanner:
        return "👺 " 
    elif claimed.lower() in roles.cult:
        return "👤 " 
    elif claimed.lower() in roles.thief:
        return "😈 " 
    elif claimed.lower() in roles.ppm:
        return "🕴 " 
    elif claimed.lower() in roles.dg:
        return "🎭 " 
    elif claimed.lower() in roles.sk:
        return "🔪 " 
    elif claimed.lower() in roles.bw:
        return "🐺🌑 " 
    elif claimed.lower() in roles.necro:
        return "⚰️ " 
    elif claimed.lower() in roles.seerfool:
        return "¿👳🃏? " 
    #custom
    elif claimed.lower() in roles.rago:
        return "🦖 " 
    elif claimed.lower() in roles.kinang:
        return "✨ " 
    elif claimed.lower() in roles.arnon:
        return "👴 " 
    elif claimed.lower() in roles.allie:
        return "👵 " 
    elif claimed.lower() in roles.noelle:
        return "🥵 "
    elif claimed.lower() in roles.taiga:
        return "🦋 "
    #caperu
    elif claimed.lower() in roles.herba:
        return "🍃 " 
    elif claimed.lower() in roles.farmer:
        return "👨‍🌾 " 
    elif claimed.lower() in roles.tc or claim.lower() == "town crier":
        return "📰 " 
    elif claimed.lower() in roles.healer:
        return "🌟 " 
    elif claimed.lower() in roles.pirate:
        return "🏴‍☠️ " 
    elif claimed.lower() in roles.fox:
        return "🦊 " 
    elif claimed.lower() in roles.ghost:
        return "👻 " 
    elif claimed.lower() in roles.cross:
        return "👀 " 
    elif claimed.lower() in roles.svg:
        return "😴 " 
    elif claimed.lower() in roles.atheist:
        return "👦 " 
    elif claimed.lower() in roles.baker:
        return "🥖 " 
    elif claimed.lower() in roles.librarian:
        return "📚 " 
    elif claimed.lower() in roles.dm:
        return "🏘 " 
    elif claimed.lower() in roles.ks:
        return "👨🏻‍🦳 " 
    elif claimed.lower() in roles.lunatic:
        return "🤪 " 
    elif claimed.lower() in roles.snow:
        return "🐺❄️ " 
    elif claimed.lower() in roles.rabid:
        return "🐺🤢 " 
    elif claimed.lower() in roles.speedy:
        return "🐺💨 " 
    elif claimed.lower() in roles.hungry:
        return "🐺🍖 " 
    elif claimed.lower() in roles.old:
        return "🐲 " 
    elif claimed.lower() in roles.imp:
        return "❌ " 
    elif claimed.lower() in roles.surv:
        return "⛺️ " 
    elif claimed.lower() in roles.amne:
        return "🤔 " 
    else:
        return ""