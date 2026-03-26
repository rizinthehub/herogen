import os
import replicate

print("----- REPLICATE DEBUG -----")
print("Token found:", bool(os.getenv("REPLICATE_API_TOKEN")))
print("Token prefix:", os.getenv("REPLICATE_API_TOKEN", "")[:10])
print("Replicate module path:", replicate.__file__)
print("---------------------------")

try:
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": "A small red apple on a wooden table, simple background",
            "aspect_ratio": "1:1"
        }
    )

    print("SUCCESS ✅")
    print("Output:", output)

except Exception as e:
    print("ERROR ❌")
    print(repr(e))