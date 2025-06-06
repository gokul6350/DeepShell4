import Navbar from "@/app/components/Navbar"
import Hero from "@/app/components/Hero"
import TerminalPreview from "@/app/components/TerminalPreview"
import Features from "@/app/components/Features"
import Installation from "@/app/components/Installation"
import CTA from "@/app/components/CTA"
import Footer from "@/app/components/Footer"

export default function Home() {
  return (
    <div className="relative min-h-screen">
      {/* Background gradients */}
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/90 to-background" />
        <div className="absolute right-0 top-0 h-[500px] w-[500px] bg-green-900/10 blur-[100px]" />
        <div className="absolute bottom-0 left-0 h-[500px] w-[500px] bg-green-700/10 blur-[100px]" />
      </div>

      <div className="relative z-10">
        <Navbar />
        <Hero />
        <TerminalPreview />
        <Features />
        <Installation />
        <CTA />
        <Footer />
      </div>
    </div>
  )
}
