"use client"

import { useEffect, useState } from "react"
import Image from "next/image"

export default function TerminalPreview() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  return (
    <div className="container py-16 flex justify-center">
      <div
        className={`relative rounded-lg overflow-hidden border border-green-500/30 shadow-2xl transition-all duration-1000 transform ${
          isVisible ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
        style={{
          maxWidth: "90%",
          animation: "float 6s ease-in-out infinite",
        }}
      >
        {/* Terminal content */}
        <div className="relative">
          <Image
            src="https://raw.githubusercontent.com/gokul6350/DeepShell4/main/preview/preview1.png"
            alt="DeepShell4 Terminal Interface"
            width={1200}
            height={800}
            className="w-full h-auto"
          />

          {/* Glow effect */}
          <div className="absolute inset-0 bg-gradient-to-tr from-green-500/10 via-green-300/5 to-transparent pointer-events-none"></div>
        </div>
      </div>
    </div>
  )
}
