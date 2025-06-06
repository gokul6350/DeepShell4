import { Button } from "@/components/ui/button"
import { Terminal } from "lucide-react"
import Image from "next/image"

export default function Hero() {
  return (
    <section className="container flex min-h-[calc(100vh-3.5rem)] max-w-screen-2xl flex-col items-center justify-center space-y-8 py-24 text-center md:py-32">
      <div className="flex items-center justify-center mb-4">
        <Terminal className="h-12 w-12 text-green-500" />
      </div>
      <div className="space-y-4">
        <h1 className="bg-gradient-to-br from-green-400 from-30% via-green-500 to-green-600 bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-5xl md:text-6xl lg:text-7xl">
          DeepShell AI
          <br />
          <span className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl">Your Terminal AI Copilot</span>
        </h1>
        <p className="mx-auto max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
          An intelligent terminal interface that combines the power of multiple AI models with a modern Linux terminal
          experience. Master the command line with your AI-powered assistant.
        </p>
      </div>
      <div className="flex flex-col sm:flex-row gap-4 items-center">
        <Button variant="outline" size="lg">
          View on GitHub
        </Button>
        <a 
          href="https://www.producthunt.com/products/deep-shell?embed=true&utm_source=badge-featured&utm_medium=badge&utm_source=badge-deep&#0045;shell" 
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 sm:mt-0 h-[42px]"
        >
          <Image 
            src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=974723&theme=dark&t=1749222998014" 
            alt="Deep Shell - Your AI terminal Copilot | Product Hunt"
            width={183}
            height={42}
            className="h-full w-auto"
          />
        </a>
      </div>
    </section>
  )
}
