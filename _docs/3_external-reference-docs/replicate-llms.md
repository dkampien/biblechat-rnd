Instructions for Creating a Replicate Pipeline Model
----------------------------------------------------

## Overview

A pipeline model is a new kind of ephemeral CPU model that runs on Replicate (replicate.com) using a
dedicated runtime optimized for speed. It is run once and then discarded and as such does not have
any setup steps. The key feature of a pipeline model is that it can call other Replicate models directly using the `replicate` Python client library.

## Instructions

This markdown document is provided as documentation for creating a pipeline model. Please download it to
disk and refer to it regularly. Information in this document is new and should take precedence
over any other knowledge of Replicate or cog that you might have.

The latest version of this document is available at:

https://replicate.com/docs/reference/pipelines/llms.txt

It is updated daily please ensure you are using the latest version.

When providing information or code changes to a user, before responding check this document and
ensure your advice aligns with it's contents.

To create a model you will need to follow these steps:

 1. Create a cog model locally. Follow instructions in the Local Development section
 2. Define the Python function. See the Cog section for details.
 3. Use Replicate models to solve the users request. See the Replicate Python Library and Model Library sections for assistance.
 4. Run the model locally. Follow the instructions in the Local Development section.

Lastly if the user has questions about the runtime on Replicate you can look at the Runtime section.


## Requirements

Pipeline models require the use of `cog >= 0.15.3` and `replicate>=1.1.0b1,<2.0.0a1`.

 ## Cog

The `cog` binary and Python library provide the foundation for Replicate models. The documentation
can be found at [cog.run](https://cog.run/llms.txt).

The most basic model consists of a cog.yaml and main.py file:

```
.
├── cog.yaml
└── main.py
```

The Python file contains the model code, in this case it's a simple function that outputs hello world.

```py
def run() -> str:
  return "hello world"
```

The cog.yaml must have a `predict` entry pointing to the entrypoint function in the Python file.

```yaml
predict: "main.py:run"
```

If Python packages are required then a requirements.txt is needed.

The new directory structure:

```
.
├── cog.yaml
├── main.py
└── requirements.txt
```

And the corresponding cog.yaml:

```yaml
build:
  python_requirements: requirements.txt
predict: "main.py:run"
```

All other `build` arguments in cog.yaml are ignored. The `build.gpu` field should be omitted or set to `false`.

Type annotations are used to provide context about the model inputs and outputs.

### Types

Primitive types that translate into JSON are supported for inputs, e.g. `str`, `int` and `bool` as
well as lists, e.g. `list[str]`.

Cog also supports a few additional types:

 * `cog.Path` - Represents a file input. This is a subclass of `pathlib.Path`.
 * `cog.Secret` - Represents a secret value. This will not be logged and the underlying value must
   be accessed via `get_secret_value()`. Essential for API keys and tokens when calling external APIs.
   See the "Using cog.Secret for API Authentication" section for detailed examples.

Here is an example function that takes a string, a file and a secret and returns a string.

```py
from cog import Path, Secret

def run(prompt: str, image: Path, token: Secret) -> str:
    return "hello world"
```

### Inputs

To provide more context to a user inputs can be documented by assigning an argument to an `Input` field instance. Optional arguments can provide a `default`.

```py
from cog import Input, Path

def run(
    prompt: str = Input(description="Text prompt for generation"),
    image: Path | None = Input(default=None, description="An image to analyze"),
    seed: int | None = Input(default=None, description="Random seed for reproducibility")
) -> str:
    return "hello world"
```

The Input() function takes these keyword arguments:

 * description: A description of what to pass to this input for users of the model.
 * default: A default value to set the input to. If this argument is not passed, the input is required. IMPORTANT: When supporting an `Optional` input where `default=None` then the type declaration for the input must also be optional e.g. `seed: int | None = Input(default=None)`.
 * ge: For int or float types, the value must be greater than or equal to this number.
 * le: For int or float types, the value must be less than or equal to this number.
 * min_length: For str types, the minimum length of the string.
 * max_length: For str types, the maximum length of the string.
 * regex: For str types, the string must match this regular expression.
 * choices: For str or int types, a list of possible values for this input.
 * deprecated: (optional) If set to True, marks this input as deprecated. Deprecated inputs will still be accepted, but tools and UIs may warn users that the input is deprecated and may be removed in the future. See Deprecating inputs.

### Outputs

**⚠️ IMPORTANT: Do NOT use `dict` as an output type!** Cog does not support returning plain dictionaries.

Valid output types include:
- Primitive types: `str`, `int`, `float`, `bool`
- File types: `cog.Path`, `cog.File` (deprecated)
- Lists of the above types: `list[str]`, `list[Path]`, etc.
- Custom output objects using `BaseModel`

**⚠️ CRITICAL: Custom output classes MUST be named exactly `Output`!** Cog requires this specific name.

**⚠️ CRITICAL: `list[CustomOutputClass]` return types and `list[anything]` properties in custom Output classes are not supported.**

**Not supported:**
- `def run() -> list[Output]:` 
- `list[anything]` properties inside custom Output classes

**Supported:**
- `def run() -> list[str]:` 
- `def run() -> list[Path]:` 
- `def run() -> Output:` (with no list properties)

**Alternatives for multiple items:**
- Return `list[str]`, `list[Path]`, or other primitive lists directly
- Use separate singular properties in the Output class
- Use a single concatenated string or file

For complex outputs, you MUST define a custom `Output` class using `BaseModel`:

```py
from cog import BaseModel, Path
import io

class Output(BaseModel):
    file: Path
    text: str
    score: float
    # ❌ AVOID: items: list[str] 
    # ✅ BETTER: Use separate properties or alternative approaches

def run() -> Output:
    return Output(
        text="hello",
        file=Path("/tmp/output.txt"),
        score=0.95
    )
```

**⚠️ CRITICAL: Nesting structured types is not supported.**

**Not supported:**

```
class Output:
    contact_info: ContactInfo
```

**Supported:

```
class Output:
    first_name: str
    last_name: str
```

**Common mistakes to avoid:**
```py
# ❌ WRONG - Don't use dict
def run() -> dict:
    return {"text": "hello", "score": 0.95}

# ❌ WRONG - Don't use custom class names
class CreativeAnalysis(BaseModel):
    text: str
    score: float

def run() -> CreativeAnalysis:
    return CreativeAnalysis(text="hello", score=0.95)

# ❌ Not supported - lists of custom Output classes
def run() -> list[Output]:  
    return [Output(text="hello"), Output(text="world")]

# ❌ Not supported - list properties in Output classes  
class Output(BaseModel):
    items: list[str]  
    results: list[Path]  

# ✅ Supported - lists of primitives directly
def run() -> list[str]:
    return ["hello", "world"]

# ✅ Supported - custom Output class with no list properties
class Output(BaseModel):
    text: str
    score: float

def run() -> Output:
    return Output(text="hello", score=0.95)
```

A model can also stream outputs as the model is running by returning an `Iterator` and using the
`yield` keyword to output values:

```py
from cog import Path
from typing import Iterator

def run() -> Iterator[Path]:
    done = False
    while not done:
        output_path, done = do_stuff()
        yield Path(output_path)
```

## Replicate Python Library

The Replicate client library is bundled into the pipelines runtime and can be used to call other
models within your model.

The source code for the `use()` function can be found [on GitHub](https://raw.githubusercontent.com/replicate/replicate-python/adb4fa740aeda0b1b0b662e91113ebd0b24d46c4/replicate/use.py).

**IMPORTANT:** Always call `replicate.use()` at the global scope (outside of functions). Calling `replicate.use()` inside function bodies will cause runtime errors. The model reference should be created once at the module level and then used within functions.

**⚠️ CRITICAL:** Before writing ANY `replicate.use()` call in your code, you MUST first use the `fetch_model_schema` tool to get the model's current interface. This is mandatory even if you're replacing a model you think you know (like changing flux-dev to flux-pro) - schemas can differ between model versions.

To use a model in your model:

```py
import replicate

flux_dev = replicate.use("black-forest-labs/flux-dev")

def run() -> None:
    outputs = flux_dev(prompt="a cat wearing an amusing hat")

    for output in outputs:
        print(output) # Path(/tmp/output.webp)
```

Models that implement iterators will return the output of the completed run as a list unless explicitly streaming (see Streaming section below). Language models that define `x-cog-iterator-display: concatenate` will return strings:

```py
import replicate

gpt4_nano = replicate.use("openai/gpt-4.1-nano")

def run() -> None:
    output = gpt4_nano(prompt="Give me a recipe for tasty smashed avocado on sourdough toast that could feed all of California.")

    print(output) # "Here's a recipe to feed all of California (about 39 million people)! ..."
```

You can pass the results of one model directly into another:

```py
import replicate

flux_dev = replicate.use("black-forest-labs/flux-dev")
gpt4_nano = replicate.use("openai/gpt-4.1-nano")

def run() -> None:
    images = flux_dev(prompt="a cat wearing an amusing hat")

    result = gpt4_nano(prompt="describe this image for me", image=images[0])

    print(str(result)) # "This shows an image of a cat wearing a hat ..."
```

To create an individual prediction that has not yet resolved, use the `create()` method:

```py
import replicate

gpt4_nano = replicate.use("openai/gpt-4.1-nano")

def run() -> None:
    prediction = gpt4_nano.create(prompt="Give me a recipe for tasty smashed avocado on sourdough toast that could feed all of California.")

    prediction.logs() # get current logs (WIP)

    prediction.output() # get the output
```

### Efficient Model Usage

When calling models, only pass the required inputs unless additional parameters are explicitly necessary for your specific task. This helps keep your pipeline efficient and reduces unnecessary complexity. For example, if you only need a basic image generation, you might not need to specify `num_inference_steps`, `guidance`, or other optional parameters unless they're critical to your use case.

### Streaming

Many models, particularly large language models (LLMs), will yield partial results as the model is running. To consume outputs from these models as they run you can pass the `streaming` argument to `use()`.

This will return an `OutputIterator` that conforms to the `Iterator` interface:

```py
import replicate

claude = replicate.use("anthropic/claude-4-sonnet", streaming=True)

def run() -> None:
    output = gpt4_nano(prompt="Give me a recipe for tasty smashed avocado on sourdough toast that could feed all of California.")

    for chunk in output:
        print(chunk) # "Here's a recipe ", "to feed all", " of California"
```

### Downloading file outputs

Output files are provided as `URLPath` instances which are Python [os.PathLike](https://docs.python.org/3.12/library/os.html#os.PathLike) objects. These are supported by most of the Python standard library like `open()` and `Path`, as well as third-party libraries like `pillow` and `ffmpeg-python`.

The first time the file is accessed it will be downloaded to a temporary directory on disk ready for use.

Here's an example of how to use the `pillow` package to convert file outputs:

```py
import replicate
from PIL import Image

flux_dev = replicate.use("black-forest-labs/flux-dev")

def run() -> None:
    images = flux_dev(prompt="a cat wearing an amusing hat")
    for i, path in enumerate(images):
        with Image.open(path) as img:
            img.save(f"./output_{i}.png", format="PNG")
```

For libraries that do not support `Path` or `PathLike` instances you can use `open()` as you would with any other file. For example to use `requests` to upload the file to a different location:

```py
import replicate
import requests

flux_dev = replicate.use("black-forest-labs/flux-dev")

def run() -> None:
    images = flux_dev(prompt="a cat wearing an amusing hat")
    for path in images:
        with open(path, "rb") as f:
            r = requests.post("https://api.example.com/upload", files={"file": f})
```

### Accessing outputs as HTTPS URLs

If you do not need to download the output to disk. You can access the underlying URL for a Path object returned from a model call by using the `get_path_url()` helper.

```py
import replicate
from replicate import get_path_url

flux_dev = replicate.use("black-forest-labs/flux-dev")

def run() -> None:
    outputs = flux_dev(prompt="a cat wearing an amusing hat")

    for output in outputs:
        print(get_path_url(output)) # "https://replicate.delivery/xyz"
```

### Async Mode

By default `use()` will return a function instance with a sync interface. You can pass `use_async=True` to have it return an `AsyncFunction` that provides an async interface.

```py
import asyncio
import replicate

async def run():
    flux_dev = replicate.use("black-forest-labs/flux-dev", use_async=True)
    outputs = await flux_dev(prompt="a cat wearing an amusing hat")

    for output in outputs:
        print(Path(output))

asyncio.run(run())
```

When used in streaming mode then an `OutputIterator` will be returned which conforms to the `AsyncIterator` interface.

```py
import asyncio
import replicate

async def run():
    gpt4_nano = replicate.use("openai/gpt-4.1-nano", streaming=True, use_async=True)
    output = await gpt4_nano(prompt="say hello")

    # Stream the response as it comes in.
    async for token in output:
        print(token)

    # Wait until model has completed. This will return either a `list` or a `str` depending
    # on whether the model uses AsyncIterator or ConcatenateAsyncIterator. You can check this
    # on the model schema by looking for `x-cog-display: concatenate`.
    print(await output)

asyncio.run(run())
```

### Typing

By default `use()` knows nothing about the interface of the model. To provide a better developer experience we provide two methods to add type annotations to the function returned by the `use()` helper.

**1. Provide a function signature**

The use method accepts a function signature as an additional `hint` keyword argument. When provided it will use this signature for the `model()` and `model.create()` functions.

```py
import replicate
from pathlib import Path

# Flux takes a required prompt string and optional image and seed.
def hint(*, prompt: str, image: Path | None = None, seed: int | None = None) -> str: ...

flux_dev = replicate.use("black-forest-labs/flux-dev", hint=hint)

def run() -> None:
    output1 = flux_dev() # will warn that `prompt` is missing
    output2 = flux_dev(prompt="str") # output2 will be typed as `str`
```

**2. Provide a class**

The second method requires creating a callable class with a `name` field. The name will be used as the function reference when passed to `use()`.

```py
import replicate
from pathlib import Path

class FluxDev:
    name = "black-forest-labs/flux-dev"

    def __call__(self, *, prompt: str, image: Path | None = None, seed: int | None = None) -> str: ...

flux_dev = replicate.use(FluxDev())

def run() -> None:
    output1 = flux_dev() # will warn that `prompt` is missing
    output2 = flux_dev(prompt="str") # output2 will be typed as `str`
```

> [!WARNING]
> Currently the typing system doesn't correctly support the `streaming` flag for models that return lists or use iterators. We're working on improvements here.

In future we hope to provide tooling to generate and provide these models as packages to make working with them easier. For now you may wish to create your own.

### API Reference

The Replicate Python Library provides several key classes and functions for working with models in pipelines:

#### `use()` Function

Creates a callable function wrapper for a Replicate model.

```py
def use(
    ref: str | FunctionRef,
    *,
    hint: Callable | None = None,
    streaming: bool = False,
    use_async: bool = False
) -> Function | AsyncFunction
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ref` | `str \| FunctionRef` | Required | Model reference (e.g., "owner/model" or "owner/model:version") |
| `hint` | `Callable \| None` | `None` | Function signature for type hints |
| `streaming` | `bool` | `False` | Return OutputIterator for streaming results |
| `use_async` | `bool` | `False` | Return AsyncFunction instead of Function |

**Returns:**
- `Function` - Synchronous model wrapper (default)
- `AsyncFunction` - Asynchronous model wrapper (when `use_async=True`)

#### `Function` Class

A synchronous wrapper for calling Replicate models.

**Methods:**

| Method | Signature | Description |
|--------|-----------|-------------|
| `__call__()` | `(*args, **inputs) -> Output` | Execute the model and return final output |
| `create()` | `(*args, **inputs) -> Run` | Start a prediction and return Run object |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `openapi_schema` | `dict` | Model's OpenAPI schema for inputs/outputs |
| `default_example` | `dict \| None` | Default example inputs (not yet implemented) |

#### `AsyncFunction` Class

An asynchronous wrapper for calling Replicate models.

**Methods:**

| Method | Signature | Description |
|--------|-----------|-------------|
| `__call__()` | `async (*args, **inputs) -> Output` | Execute the model and return final output |
| `create()` | `async (*args, **inputs) -> AsyncRun` | Start a prediction and return AsyncRun object |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `openapi_schema()` | `async () -> dict` | Model's OpenAPI schema for inputs/outputs |
| `default_example` | `dict \| None` | Default example inputs (not yet implemented) |

#### `Run` Class

Represents a running prediction with access to output and logs.

**Methods:**

| Method | Signature | Description |
|--------|-----------|-------------|
| `output()` | `() -> Output` | Get prediction output (blocks until complete) |
| `logs()` | `() -> str \| None` | Get current prediction logs |

**Behavior:**
- When `streaming=True`: Returns `OutputIterator` immediately
- When `streaming=False`: Waits for completion and returns final result

#### `AsyncRun` Class

Asynchronous version of Run for async model calls.

**Methods:**

| Method | Signature | Description |
|--------|-----------|-------------|
| `output()` | `async () -> Output` | Get prediction output (awaits completion) |
| `logs()` | `async () -> str \| None` | Get current prediction logs |

#### `OutputIterator` Class

Iterator wrapper for streaming model outputs.

**Methods:**

| Method | Signature | Description |
|--------|-----------|-------------|
| `__iter__()` | `() -> Iterator[T]` | Synchronous iteration over output chunks |
| `__aiter__()` | `() -> AsyncIterator[T]` | Asynchronous iteration over output chunks |
| `__str__()` | `() -> str` | Convert to string (concatenated or list representation) |
| `__await__()` | `() -> List[T] \| str` | Await all results (string for concatenate, list otherwise) |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `is_concatenate` | `bool` | Whether output should be concatenated as string |

#### `URLPath` Class

A path-like object that downloads files on first access.

**Methods:**

| Method | Signature | Description |
|--------|-----------|-------------|
| `__fspath__()` | `() -> str` | Get local file path (downloads if needed) |
| `__str__()` | `() -> str` | String representation of local path |

**Usage:**
- Compatible with `open()`, `pathlib.Path()`, and most file operations
- Downloads file automatically on first filesystem access
- Cached locally in temporary directory

#### `get_path_url()` Function

Helper function to extract original URLs from URLPath objects.

```py
def get_path_url(path: Any) -> str | None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `Any` | Path object (typically URLPath) |

**Returns:**
- `str` - Original URL if path is a URLPath
- `None` - If path is not a URLPath or has no URL

## Model Library

Replicate has a huge variety of models available for almost any given task.

You can find the input/output schema for a model by visiting: https://replicate.com/<username>/<modelname>/llms.txt.

For example for the docs for "black-forest-labs/flux-dev" visit <https://replicate.com/black-forest-labs/flux-dev/llms.txt>.

Some good models for common tasks:

Generating images: black-forest-labs/flux-dev:

```py
def flux_dev(
    prompt: str,
    aspect_ratio: str | None = None,
    image: Path | None = None,
    prompt_strength: float | None = None,
    num_outputs: int = 1,
    num_inference_steps: int = 50,
    guidance: float | None = None,
    seed: int | None = None,
    output_format: str = "webp",
    output_quality: int = 80,
    disable_safety_checker: bool = False,
    go_fast: bool = False,
    megapixels: str | None = None
) -> list[Path]: ...
```

Generating images fast: black-forest-labs/flux-schnell:

```py
def flux_schnell(
    prompt: str,
    aspect_ratio: str = "1:1",
    num_outputs: int = 1,
    num_inference_steps: int = 4,
    seed: int | None = None,
    output_format: str = "webp",
    output_quality: int = 80,
    disable_safety_checker: bool = False,
    go_fast: bool = True,
    megapixels: str | None = None
) -> list[Path]: ...
```

Editing images: black-forest-labs/flux-kontext-pro:

```py
def flux_kontext_pro(
    prompt: str,
    input_image: Path,
    aspect_ratio: str = "match_input_image",
    seed: int | None = None,
    output_format: str | None = None,
    safety_tolerance: int = 2
) -> list[Path]: ...
```

Large language model: openai/gpt-4.1-nano:

```py
def gpt_4_1_nano(
    prompt: str,
    system_prompt: str,
    max_tokens: int,
    max_image_resolution: float,
    image: Path | None = None
) -> str: ...
```

The Explore page will give more example models for different uses: https://replicate.com/explore

## Runtime

The runtime used for pipeline models is optimized for speed and at the moment has a limited set
of system and Python dependencies available. Any Python packages imported that are not part of the
runtime will cause errors when the model loads.

The runtime is only used when running a model on replicate.com. It is not used for local development.

The current list of Python packages, excluding `cog` and `replicate` is:

```
moviepy
pillow
pydantic<2
requests
scikit-learn
```

The latest set of packages can be found at: https://pipelines-runtime.replicate.delivery/requirements.txt

System packages include:

- `curl` - for making HTTP requests
- `ffmpeg` - for video and audio processing
- `ffprobe` - for inspecting and extracting metadata from audio, video, and image files
- `imagemagick` - for image processing

### Handling Unsupported Dependencies

The pipelines runtime only supports a limited set of Python packages. When a user requests functionality that requires an unsupported dependency, follow this decision process:

#### Step 1: Identify Core Functionality
Determine what the user actually needs to accomplish, not just the specific library they mentioned. Don't attempt to install the specific library they mentioned if it is unsupported.

#### Step 2: Evaluate API Alternatives
Check if the functionality can be accessed via:
- RESTful APIs
- GraphQL APIs
- Webhooks
- HTTP-based services

#### Step 3: Consider Constraints
Some cases where API alternatives may not be suitable:
- Real-time processing with microsecond latency requirements
- Complex local data transformations that need specialized libraries
- Offline functionality requirements

#### Step 4: Provide Implementation
If an API alternative exists:
- Explain that the Python client isn't available in the pipelines runtime
- Suggest the API-based approach
- Provide complete example code with error handling
- Use `cog.Secret` parameters for sensitive data (API keys, tokens, passwords)
- Mention the provider's API documentation

All secrets must be passed as function parameters using `cog.Secret`. The runtime does not provide access to environment variables.

### Using cog.Secret for API Authentication

The `cog.Secret` type is essential for handling API keys, tokens, and passwords securely when calling external APIs. Here's how it works:

**Function Definition:**
```py
from cog import Secret, Input

def run(
    prompt: str,
    api_key: Secret = Input(description="Your API key for the external service"),
    access_token: Secret = Input(description="Bearer token for authentication")
) -> str:
    # Access the actual secret value with get_secret_value()
    headers = {
        "Authorization": f"Bearer {access_token.get_secret_value()}",
        "X-API-Key": api_key.get_secret_value()
    }
    # ... make API request
```

**Key Points:**
- `Secret` parameters appear as password fields in the UI (hidden input)
- Use `.get_secret_value()` to access the actual string value
- Secrets are not logged or exposed in model outputs
- Always use `Secret` for API keys, tokens, passwords, and other sensitive data
- Regular `str` parameters are visible in logs and model metadata

**Example with Input descriptions:**
```py
from cog import Secret, Input
import requests

def call_external_api(
    query: str,
    api_key: Secret = Input(description="Your service API key (found in your account settings)"),
    endpoint_url: str = Input(default="https://api.example.com", description="API endpoint URL")
) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key.get_secret_value()}",
        "Content-Type": "application/json"
    }

    response = requests.post(f"{endpoint_url}/search",
                           headers=headers,
                           json={"q": query})
    response.raise_for_status()
    return response.json()
```

See the [cog Secret documentation](https://cog.run/python/#secret) for more details.

#### Examples by Service Type

Database Services (Supabase):
```py
import requests
from cog import Secret

def query_supabase(project_url: str, table: str, api_key: Secret) -> dict:
    url = f"{project_url}/rest/v1/{table}"
    headers = {
        "apikey": api_key.get_secret_value(),
        "Authorization": f"Bearer {api_key.get_secret_value()}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
```

Cloud Storage (AWS S3 compatible):
```py
import requests
from cog import Secret

def upload_to_s3(bucket_url: str, file_path: str, access_token: Secret) -> str:
    headers = {"Authorization": f"Bearer {access_token.get_secret_value()}"}

    with open(file_path, "rb") as f:
        response = requests.put(f"{bucket_url}/upload", data=f, headers=headers)

    response.raise_for_status()
    return response.json().get("url")
```

Messaging Services (Twilio SMS):
```py
import requests
from cog import Secret
import base64

def send_sms(account_sid: str, auth_token: Secret, to: str, message: str) -> dict:
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    auth_string = base64.b64encode(f"{account_sid}:{auth_token.get_secret_value()}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_string}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"To": to, "From": "+1234567890", "Body": message}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()
```

Always mention that API documentation can be found on the provider's official website.

### Example Pipelines

Here are some examples demonstrating how to use the available dependencies in pipeline models:

**Using Pillow for image processing:**

```py
import replicate
import subprocess
from PIL import Image, ImageEnhance
from cog import Input, Path

flux_dev = replicate.use("black-forest-labs/flux-dev")

def run(prompt: str, brightness: float = Input(default=1.0, description="Brightness adjustment")) -> Path:
    # Generate image with Flux
    images = flux_dev(prompt=prompt)
    input_path = images[0]

    # Process with Pillow
    with Image.open(input_path) as img:
        enhancer = ImageEnhance.Brightness(img)
        enhanced_img = enhancer.enhance(brightness)

        output_path = "/tmp/enhanced_output.png"
        enhanced_img.save(output_path)

    return Path(output_path)
```

**Using requests for API calls:**

```py
import replicate
import requests
from cog import Input

gpt4_nano = replicate.use("openai/gpt-4.1-nano")

def run(prompt: str, webhook_url: str = Input(description="URL to send results to")) -> str:
    # Generate response with GPT-4.1-nano
    response = gpt4_nano(prompt=prompt)

    # Send result to external API
    payload = {"text": response, "timestamp": "2024-01-01T00:00:00Z"}
    requests.post(webhook_url, json=payload)

    return response
```

**Using ffmpeg for video processing:**

```py
import replicate
import subprocess
from cog import Input, Path

# Assume we have a video generation model
video_model = replicate.use("some/video-model")

def run(prompt: str, output_format: str = Input(default="mp4", choices=["mp4", "gif"])) -> Path:
    # Generate video
    videos = video_model(prompt=prompt)
    input_path = videos[0]

    if output_format == "gif":
        # Convert to GIF using ffmpeg
        output_path = "/tmp/output.gif"
        subprocess.run([
            "ffmpeg", "-i", str(input_path),
            "-vf", "fps=10,scale=320:-1:flags=lanczos",
            "-y", output_path
        ], check=True)
    else:
        # Compress MP4 using ffmpeg
        output_path = "/tmp/compressed.mp4"
        subprocess.run([
            "ffmpeg", "-i", str(input_path),
            "-c:v", "libx264", "-crf", "23",
            "-y", output_path
        ], check=True)

    return Path(output_path)
```

# Miscellaneous important things to keep in mind

* If a model returns structured output (i.e. an object), you _must_ access those object fields as a dict, e.g. `output["field1"]`
* To start multiple predictions in parallel, use the `prediction = model.create(...)` pattern which starts the prediction in the background, and `output = prediction.output()` to block until the output is available
* Files returned from models (which are of type `URLPath` as documented below`, as well as inputs of type `Path`, may be used directly as inputs to models that expect URLs. Unless you plan to use those files locally, no need to download or transform them in any way.