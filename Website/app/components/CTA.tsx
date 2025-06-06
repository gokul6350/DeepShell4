import { Button } from "@/components/ui/button"
import { Terminal } from "lucide-react"

export default function CTA() {
  return (
    <section className="border-t border-border/40">
      <div className="container flex flex-col items-center gap-4 py-24 text-center md:py-32">
        <Terminal className="h-12 w-12 text-green-500 mb-4" />
        <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-5xl">
          Ready to transform your terminal experience?
        </h2>
        <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
          Join thousands of developers who have enhanced their Linux command line productivity with DeepShell4.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 mt-8">
          <Button size="lg" className="bg-green-600 hover:bg-green-700">
            Download DeepShell4
          </Button>
          <Button variant="outline" size="lg">
            Star on GitHub
          </Button>
        </div>
      </div>
    </section>
  )
}
