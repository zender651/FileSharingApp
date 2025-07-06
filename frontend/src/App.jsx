import React, { useState } from 'react'

function App() {
  const [file, setFile] = useState(null)
  const [fileUuid, setFileUuid] = useState('')
  const [downloadUuid, setDownloadUuid] = useState('')
  const [error, setError] = useState('')
  const [downloading, setDownloading] = useState(false)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setFileUuid('')
    setError('')
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/v1/upload', {
        method: 'POST',
        body: formData
      })

      if (!res.ok) {
        const { detail } = await res.json()
        throw new Error(detail || 'Upload failed')
      }

      const data = await res.json()
      setFileUuid(data.file_uuid)
      setDownloadUuid(data.file_uuid)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDownload = async () => {
    if (!downloadUuid) {
      setError('Enter a UUID to download.')
      return
    }

    setDownloading(true)
    try {
      const res = await fetch(`/api/v1/download/${downloadUuid}`)
      if (!res.ok) throw new Error('File not found or expired.')

      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `file-${downloadUuid}`
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
      setError('')
    } catch (err) {
      setError(err.message)
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>📦 FastAPI File Uploader</h1>

      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: '1rem' }}>Upload</button>

      {fileUuid && (
        <div style={{ marginTop: '1rem' }}>
          ✅ Uploaded! UUID: <code>{fileUuid}</code>
        </div>
      )}

      <hr style={{ margin: '2rem 0' }} />

      <h2>⬇️ Download a File</h2>
      <input
        type="text"
        placeholder="Enter UUID"
        value={downloadUuid}
        onChange={(e) => setDownloadUuid(e.target.value)}
        style={{ width: '300px' }}
      />
      <button
        onClick={handleDownload}
        style={{ marginLeft: '1rem' }}
        disabled={downloading}
      >
        {downloading ? 'Downloading...' : 'Download'}
      </button>

      {error && (
        <div style={{ color: 'red', marginTop: '1rem' }}>
          ❌ {error}
        </div>
      )}
    </div>
  )
}

export default App
