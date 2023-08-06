from typing import Union, Any

def printMk(txt: str):
  from IPython.display import display, Markdown
  display(Markdown(txt))

def printError(txt: str):
  printMk(f'<span style="font-weight: bold; color: #E2548A;">Error:</span> {txt}')

# From https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def sizeOfFmt(num: Union[int, Any]):
  if type(num) != int: return ""
  numLeft: float = num
  for unit in ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
    if abs(numLeft) < 1000.0:
      return f"{numLeft:3.0f} {unit}"
    numLeft /= 1000.0
  return f"{numLeft:.1f} YB"

def formatImageTag(imageUrl: Union[str, None], imageAltText: Union[str, None]):
  imageUrl = imageUrl if imageUrl else "https://app.modelbit.com/images/profile-placeholder.png"
  return (
    f'<img src="{ imageUrl }" '
    f'alt="{ imageAltText }" '
    f'style="display:inline-block;border-radius:9999px;width:2rem;height:2rem;background-color: rgb(229 231 235);" />'
  )
