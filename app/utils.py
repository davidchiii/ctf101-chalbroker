import os, subprocess

def find_dockerfiles() -> dict:
    """Returns a dict{} of all Dockerfiles in the /challenges directory. Run once so I can store in memory."""
    res = {}
    for path, dirs, files in os.walk("challenges"):
        for file in files:
            if file == "Dockerfile":
                full_path = os.path.join(path, file).removesuffix("Dockerfile")
                rel_path = os.path.relpath(full_path, "challenges")
                folder = os.path.relpath(path, "challenges")
                res[folder] = full_path.removesuffix("Dockerfile")
    return res

def check_system() -> bool:
    """This function checks the local system to see if the required tools are installed."""
    req = ["docker", "curl"]

    def is_tool(name):
        from shutil import which
        return which(name) is not None
    print("🔎 Checking for required system utils....")
    try:
        for i in req:
            print(f"Checking {i}")
            if not is_tool(i):
                raise Exception(f"{i} not found.")
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("✅ No missing system utils.")
    print("\n")


# @param name
# @param path
def run_build(name, path):
    """Attempts to build {path}, tagging the image as {name}."""
    try:
        res = subprocess.run(
            ["docker", "build", "-t", name, path],
            check=True,          # raises error if build fails
            capture_output=True,
            text=True
        )
        print(f"✅ Build succeeded for {name}")
    except subprocess.CalledProcessError as e:
        print(f"Build failed for {name}")
        print(e.stderr or e.stdout)
