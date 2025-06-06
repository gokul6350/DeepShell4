import { Button } from "@/components/ui/button"
import { Copy } from "lucide-react"

export default function Installation() {
  return (
    <div id="installation" className="bg-black/30 py-24">
      <div className="container">
        <div className="mx-auto max-w-[58rem] text-center mb-12">
          <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-5xl">Easy Installation</h2>
          <p className="mt-4 text-muted-foreground sm:text-lg">Get up and running with DeepShell4 in minutes</p>
        </div>

        <div className="mx-auto max-w-3xl rounded-lg border bg-black/50 p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm text-gray-400">Terminal</div>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
              <Copy className="h-4 w-4" />
            </Button>
          </div>
          <pre className="font-mono text-green-500 p-4 overflow-x-auto">
            <code>
              # Install DeepShell4{"\n"}
              wget https://github.com/gokul6350/DeepShell4/blob/main/deepshell.deb{"\n"}
              sudo dpkg -i deepshell.deb{"\n\n"}# Launch DeepShell4{"\n"}
              deepshell
            </code>
          </pre>
        </div>

        <div className="mt-12 text-center">
          <Button size="lg" className="bg-green-600 hover:bg-green-700">
            View Full Documentation
          </Button>
        </div>
      </div>
    </div>
  )
}
