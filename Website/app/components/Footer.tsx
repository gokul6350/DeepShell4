import Link from "next/link"
import { Github, Twitter, DiscIcon as Discord } from "lucide-react"

export default function Footer() {
  return (
    <footer className="border-t border-border/40">
      <div className="container flex flex-col gap-8 py-8 md:flex-row md:py-12">
        <div className="flex-1 space-y-4">
          <h2 className="font-bold text-green-500">DeepShell AI</h2>
          <p className="text-sm text-muted-foreground">Your AI-powered terminal copilot for Linux systems.</p>
        </div>
        <div className="grid flex-1 grid-cols-2 gap-12 sm:grid-cols-3">
          <div className="space-y-4">
            <h3 className="text-sm font-medium">Project</h3>
            <ul className="space-y-3 text-sm">
              <li>
                <Link href="#features" className="text-muted-foreground transition-colors hover:text-green-500">
                  Features
                </Link>
              </li>
              <li>
                <Link href="#installation" className="text-muted-foreground transition-colors hover:text-green-500">
                  Installation
                </Link>
              </li>
              <li>
                <Link href="/roadmap" className="text-muted-foreground transition-colors hover:text-green-500">
                  Roadmap
                </Link>
              </li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-sm font-medium">Resources</h3>
            <ul className="space-y-3 text-sm">
              <li>
                <Link href="/docs" className="text-muted-foreground transition-colors hover:text-green-500">
                  Documentation
                </Link>
              </li>
              <li>
                <Link href="/tutorials" className="text-muted-foreground transition-colors hover:text-green-500">
                  Tutorials
                </Link>
              </li>
              <li>
                <Link href="/api" className="text-muted-foreground transition-colors hover:text-green-500">
                  API Reference
                </Link>
              </li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-sm font-medium">Connect</h3>
            <div className="flex space-x-4">
              <Link
                href="https://github.com/gokul6350/DeepShell4"
                className="text-muted-foreground transition-colors hover:text-green-500"
              >
                <Github className="h-5 w-5" />
                <span className="sr-only">GitHub</span>
              </Link>
              <Link
                href="https://twitter.com/deepshell4"
                className="text-muted-foreground transition-colors hover:text-green-500"
              >
                <Twitter className="h-5 w-5" />
                <span className="sr-only">Twitter</span>
              </Link>
              <Link
                href="https://discord.gg/deepshell4"
                className="text-muted-foreground transition-colors hover:text-green-500"
              >
                <Discord className="h-5 w-5" />
                <span className="sr-only">Discord</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
      <div className="container border-t border-border/40 py-6">
        <p className="text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} DeepShell4. Open source under MIT License.
        </p>
      </div>
    </footer>
  )
}
