from . import *

if not os.path.exists("CODES"):
    os.makedirs("CODES")

path = os.path.join(os.getcwd(), "CODES")


@click.command()
@click.argument("code", required=True, default="codehere")
@click.argument("group", required=False, default="default")
def commander(code, group):
    if str(code) == 'nhentaichive':
        r = requests.get(f"https://nhentaichive.johnlester.repl.co/group/{group}").text
        codes = json.loads(r)["code"]
        for i, code in enumerate(codes):
            info = NHentai(code)
            info.save_images(debug=True)
            msg = "\n" + f"[NHentaiDevs] : Part {i+1} out of {len(codes)} done :>" + "\n"
            print(cl.colorize(msg, [randint(50, 255), randint(50, 255), randint(50, 255)]))
        
        return

    if str(code) == 'init':
        toml_str = """
# Initialization for Nhentaidevs :>

[Nhentai]
codes=[] # Insert your code/s in the 'codes' block (Use ',' for multi-codes)

# Example:
# codes=[177013, 228922, 4299]"""
        with open("CodesHere.code", "w") as f:
            f.write(toml_str)

        print(cl.colorize(
                "[NHentaiDevs] : CodesHere.code has been created, ready for your codes :>",
                [randint(50, 255), randint(50, 255), randint(50, 255)]))

        return
    if str(code) == "codehere":
        if os.path.exists("CodesHere.code"):
            with open("CodesHere.code", "r") as f:
                codes = toml.loads(f.read())["Nhentai"]["codes"]
                if codes:
                    for i, code in enumerate(codes):
                        info = NHentai(code)
                        info.save_images(debug=True)
                        msg = "\n" + f"[NHentaiDevs] : Part {i+1} out of {len(codes)} done :>" + "\n"
                        print(cl.colorize(msg, [randint(50, 255), randint(50, 255), randint(50, 255)]))
                else:
                    print(cl.colorize(
                "[NHentaiDevs] : No code/s was found in CodesHere.code, put at least one.",
                [randint(50, 255), randint(50, 255), randint(50, 255)]))
                    return

            os.remove("CodesHere.code")

            return
        else:
            print(cl.colorize(
                "[NHentaiDevs] : No CodesHere.code file found, run python(or python3) -m nhentaidevs init",
                [randint(50, 255), randint(50, 255), randint(50, 255)]))
            return

        
    
    NHentai(code).save_images(debug=True)


if __name__ == "__main__":
    commander()


