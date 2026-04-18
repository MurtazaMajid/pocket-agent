# 🤖 Pocket-Agent — On-device Tool-Calling Assistant

A fine-tuned TinyLlama 1.1B model for structured tool calling, optimized to run fully offline on mobile devices.

## 🏆 Hackathon Submission — Pocket-Agent

**Base model:** TinyLlama/TinyLlama-1.1B-Chat-v1.0  
**Parameters:** 1.1B (≤2B requirement ✅)  
**Quantized size:** ~350MB (≤500MB requirement ✅)  
**Fine-tuning method:** LoRA (r=8, alpha=16)  
**Training examples:** 1,090 balanced synthetic examples  

---

## 🛠️ Supported Tools

| Tool | Trigger | Example |
|------|---------|---------|
| `weather` | Temperature, forecast, rain queries | "What's the weather in Karachi?" |
| `calendar` | List or create events | "Schedule dentist on 2025-09-10" |
| `convert` | Physical unit conversion | "Convert 100 km to miles" |
| `currency` | Money/exchange conversion | "How much is 500 USD in PKR?" |
| `sql` | Database queries | "Show all active users" |

---

## 📤 Output Format

For tool calls:
```json
<tool_call>{"tool": "weather", "args": {"location": "Karachi", "unit": "C"}}</tool_call>
```

For unsupported requests:
