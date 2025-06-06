"use client"

import { useEffect, useState } from "react"
import Image from "next/image"

export default function TerminalPreview() {
  const [isVisible, setIsVisible] = useState(false)
  const [text, setText] = useState("")
  const fullText = "$ deepshell --help"

  useEffect(() => {
    setIsVisible(true)

    // Typing animation
    let i = 0
    const typingInterval = setInterval(() => {
      if (i < fullText.length) {
        setText(fullText.substring(0, i + 1))
        i++
      } else {
        clearInterval(typingInterval)
      }
    }, 100)

    return () => clearInterval(typingInterval)
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
        {/* Terminal header */}
        <div className="bg-gray-900 px-4 py-2 flex items-center">
          <div className="flex space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <div className="mx-auto text-sm text-gray-400">DeepShell4 Terminal</div>
        </div>

        {/* Terminal content */}
        <div className="relative">
          <Image
            src="https://raw.githubusercontent.com/gokul6350/DeepShell4/main/preview/preview1.png"
            alt="DeepShell4 Terminal Interface"
            width={1200}
            height={800}
            className="w-full h-auto"
          />

          {/* Overlay with typing effect */}
          <div className="absolute top-0 left-0 p-4">
            <span className="text-green-500 font-mono">{text}</span>
            <span
              className={`inline-block w-2 h-5 bg-green-500 ml-1 ${text.length === fullText.length ? "animate-pulse" : ""}`}
            ></span>
          </div>

          {/* Glow effect */}
          <div className="absolute inset-0 bg-gradient-to-tr from-green-500/10 via-green-300/5 to-transparent pointer-events-none"></div>
        </div>
      </div>
    </div>
  )
}
