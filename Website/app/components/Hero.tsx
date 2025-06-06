import { Button } from "@/components/ui/button"
import { ArrowRight, Terminal } from "lucide-react"

export default function Hero() {
  return (
    <section className="container flex min-h-[calc(100vh-3.5rem)] max-w-screen-2xl flex-col items-center justify-center space-y-8 py-24 text-center md:py-32">
      <div className="flex items-center justify-center mb-4">
        <Terminal className="h-12 w-12 text-green-500" />
      </div>
      <div className="space-y-4">
        <h1 className="bg-gradient-to-br from-green-400 from-30% via-green-500 to-green-600 bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-5xl md:text-6xl lg:text-7xl">
          DeepShell4
          <br />
          <span className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl">Your Terminal Copilot</span>
        </h1>
        <p className="mx-auto max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
          An intelligent terminal interface that combines the power of multiple AI models with a modern Linux terminal
          experience. Master the command line with your AI-powered assistant.
        </p>
      </div>
      <div className="flex gap-4">
        <Button size="lg" className="bg-green-600 hover:bg-green-700">
          Get Started
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
        <Button variant="outline" size="lg">
          View on GitHub
        </Button>
      </div>
    </section>
  )
}
