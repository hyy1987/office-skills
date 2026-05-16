import argparse
import base64
import os
import sys
import urllib.request
from pathlib import Path
from typing import Iterable

from openai import OpenAI


DEFAULT_ENV_KEY = "OPENAI_API_KEY"
DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1536x1024"

DEFAULT_PROMPT_SUFFIX = """\

PPT slide image requirements:
- Generate exactly one presentation slide image.
- Keep the slide clean, readable, and suitable for screen sharing.
- Preserve all user-provided text exactly when text is requested.
- Keep text concise and well aligned.
- Avoid garbled characters, watermarks, random logos, and irrelevant UI.
- Use reference images only for visual style or layout unless the prompt explicitly asks to copy content.
"""


def default_base_url() -> str:
    return os.getenv("OPENAI_BASE_URL") or DEFAULT_BASE_URL


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text()


def image_bytes_from_response(response) -> bytes:
    if not getattr(response, "data", None):
        raise RuntimeError("Image API response did not contain data.")

    item = response.data[0]
    b64_json = getattr(item, "b64_json", None)
    if b64_json:
        if b64_json.startswith("data:"):
            b64_json = b64_json.split(",", 1)[1]
        return base64.b64decode(b64_json)

    url = getattr(item, "url", None)
    if url:
        with urllib.request.urlopen(url, timeout=120) as remote:
            return remote.read()

    raise RuntimeError("Image API response contained neither b64_json nor url.")


def open_reference_images(paths: Iterable[str]):
    files = []
    try:
        for value in paths:
            image_path = Path(value).expanduser().resolve()
            if not image_path.is_file():
                raise FileNotFoundError(f"Reference image not found: {image_path}")
            files.append(image_path.open("rb"))
        return files
    except Exception:
        for file in files:
            file.close()
        raise


def build_prompt(prompt: str, suffix: str | None) -> str:
    prompt = prompt.strip()
    if not prompt:
        raise RuntimeError("Prompt is empty.")
    return f"{prompt}{suffix}" if suffix else prompt


def prompt_from_args(args: argparse.Namespace) -> tuple[str, Path | None]:
    if args.prompt_text:
        return args.prompt_text, None
    if args.stdin:
        return sys.stdin.read(), None
    if args.prompt:
        prompt_path = Path(args.prompt).expanduser().resolve()
        if not prompt_path.is_file():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        return read_text(prompt_path), prompt_path
    raise RuntimeError("Provide a prompt file, --prompt-text, or --stdin.")


def default_output_path(args: argparse.Namespace, prompt_path: Path | None) -> Path:
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    elif prompt_path:
        output_path = prompt_path.with_suffix(args.output_ext)
    else:
        output_path = Path(f"slide{args.output_ext}").resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def generate_image(client: OpenAI, prompt: str, output_path: Path, args: argparse.Namespace) -> Path:
    request = {
        "model": args.model,
        "prompt": build_prompt(prompt, None if args.no_suffix else args.prompt_suffix),
        "size": args.size,
        "n": 1,
    }
    if args.quality:
        request["quality"] = args.quality

    if args.reference_image:
        image_files = open_reference_images(args.reference_image)
        try:
            request["image"] = image_files if len(image_files) > 1 else image_files[0]
            response = client.images.edit(**request)
        finally:
            for file in image_files:
                file.close()
    else:
        response = client.images.generate(**request)

    output_path.write_bytes(image_bytes_from_response(response))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one PPT-style slide image from a prompt using an OpenAI-compatible image API."
    )
    parser.add_argument("prompt", nargs="?", help="Prompt Markdown file, typically NN-topic.md.")
    parser.add_argument("-o", "--output", help="Output image path. Defaults to prompt stem + output extension.")
    parser.add_argument("--prompt-text", help="Prompt text provided directly on the command line.")
    parser.add_argument("--stdin", action="store_true", help="Read prompt text from stdin.")
    parser.add_argument("--reference-image", action="append", default=[], help="Reference image path. Repeatable.")
    parser.add_argument(
        "--base-url",
        default=default_base_url(),
        help=f"OpenAI-compatible base URL. Default: {DEFAULT_BASE_URL}",
    )
    parser.add_argument("--env-key", default=DEFAULT_ENV_KEY, help=f"API key environment variable. Default: {DEFAULT_ENV_KEY}")
    parser.add_argument("--model", default=os.getenv("OPENAI_IMAGE_MODEL", DEFAULT_MODEL), help=f"Image model. Default: {DEFAULT_MODEL}")
    parser.add_argument("--size", default=os.getenv("PPT_IMAGE_SIZE", DEFAULT_SIZE), help=f"Image size. Default: {DEFAULT_SIZE}")
    parser.add_argument("--quality", default=os.getenv("PPT_IMAGE_QUALITY"), help="Optional image quality value.")
    parser.add_argument("--output-ext", default=".png", help="Default output extension when -o is omitted.")
    parser.add_argument("--prompt-suffix", default=DEFAULT_PROMPT_SUFFIX, help="Prompt suffix appended by default.")
    parser.add_argument("--no-suffix", action="store_true", help="Do not append the default prompt suffix.")
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        api_key = os.getenv(args.env_key)
        if not api_key:
            raise RuntimeError(f"Environment variable {args.env_key} is not set.")

        prompt, prompt_path = prompt_from_args(args)
        output_path = default_output_path(args, prompt_path)
        client = OpenAI(api_key=api_key, base_url=args.base_url)
        generate_image(client, prompt, output_path, args)
        print(f"Saved image: {output_path}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
