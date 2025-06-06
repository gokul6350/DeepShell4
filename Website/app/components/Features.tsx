import { Terminal, Brain, Zap, Code, Server, Shield } from "lucide-react"

const features = [
  {
    name: "AI-Powered Command Assistance",
    description: "Get intelligent suggestions, explanations, and corrections for your terminal commands.",
    icon: Brain,
  },
  {
    name: "Modern Terminal Interface",
    description: "Enjoy a sleek, customizable terminal experience with syntax highlighting and smart completions.",
    icon: Terminal,
  },
  {
    name: "Multi-Model Support",
    description: "Leverage multiple AI models to get the best assistance for different command-line tasks.",
    icon: Server,
  },
  {
    name: "Script Generation",
    description: "Generate shell scripts automatically based on natural language descriptions of your tasks.",
    icon: Code,
  },
  {
    name: "System Diagnostics",
    description: "Analyze system issues and get recommended solutions with AI-powered diagnostics.",
    icon: Zap,
  },
  {
    name: "Secure by Design",
    description: "All processing happens locally with optional cloud features that respect your privacy.",
    icon: Shield,
  },
]

export default function Features() {
  return (
    <section id="features" className="container space-y-16 py-24 md:py-32">
      <div className="mx-auto max-w-[58rem] text-center">
        <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-5xl">Supercharge Your Terminal</h2>
        <p className="mt-4 text-muted-foreground sm:text-lg">
          DeepShell4 transforms how you interact with the Linux command line, making you more productive and
          knowledgeable.
        </p>
      </div>
      <div className="mx-auto grid max-w-5xl grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
        {features.map((feature) => (
          <div
            key={feature.name}
            className="relative overflow-hidden rounded-lg border bg-background p-8 transition-all hover:border-green-500/50 hover:shadow-md"
          >
            <div className="flex items-center gap-4">
              <feature.icon className="h-8 w-8 text-green-500" />
              <h3 className="font-bold">{feature.name}</h3>
            </div>
            <p className="mt-2 text-muted-foreground">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
