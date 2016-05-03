str = "i ve just spent the past five hours studying g protein synthesis in cytotoxic helper t cells, does anyone know a really good way to relax?,i just got accepted to the university of iowa school of nursing finally i was so worried,wishing everyone good luck at school,omg i found out i made the dean s list today ,glad to be back in iowa city ,can t upload any photos, anyone else having this problem?,phew well i m finally done studying for my big pathophysiology test, nothing left to do but pray i do well,lol it happens to the best of us,just found out he will be spending hours a week in class next semester even though he only has credit hours. why, hours a week of clinicals. ouch,omg it s suppossed to be below tommorrow with the wind chill ,i fought, i worked, i prayed, i laughed, i cried, i cheered, in the end i triumphed,just found out that he has a performance exam over everything we covered this semester the monday after thanksgiving break, so much for resting over break :(,happy thanksgiving"
str = "this morning i went for fishing:)??"

def tokenizer(str):
    from re import sub
    word_only_str       = sub('[^a-z]', ' ', str.lower())
    expression_only_str = sub('[^:;)(]', ' ', str.lower())
    all_punctuations    = [_char for _char in sub('[a-z:;)(]', ' ', str.lower()) if _char != ' ']

    return " ".join(word_only_str.split() + expression_only_str.split() + all_punctuations)

print(tokenizer(str))
