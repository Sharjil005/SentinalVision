import { useParams, Link } from 'react-router-dom'
import { Video, Clock, CheckCircle, AlertTriangle, ArrowLeft, Download, Play } from 'lucide-react'

export default function AnalysisDetail() {
  const { id } = useParams()

  // Mock data for demonstration
  const analysis = {
    id,
    filename: 'sample_video.mp4',
    status: 'completed',
    createdAt: '2024-01-15 10:30:00',
    completedAt: '2024-01-15 10:35:22',
    duration: '2:34',
    fps: 30,
    resolution: '1920x1080',
    fileSize: '45.2 MB',
    totalFrames: 4620,
    processedFrames: 4620,
    detections: 142,
    alerts: 3,
    modelVersion: 'yolov8n + resnet18_v1',
  }

  const alerts = [
    { id: 1, type: 'person_loitering', severity: 'warning', confidence: 0.87, timestamp: '00:01:23', frame: 2490, acknowledged: false },
    { id: 2, type: 'unattended_object', severity: 'critical', confidence: 0.92, timestamp: '00:01:45', frame: 3150, acknowledged: true },
    { id: 3, type: 'crowd_gathering', severity: 'info', confidence: 0.76, timestamp: '00:02:10', frame: 3960, acknowledged: false },
  ]

  const detectionsByClass = [
    { class: 'person', count: 89 },
    { class: 'car', count: 34 },
    { class: 'truck', count: 12 },
    { class: 'bicycle', count: 7 },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'processing': return 'bg-yellow-100 text-yellow-800'
      case 'failed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200'
      case 'warning': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'info': return 'bg-blue-100 text-blue-800 border-blue-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-4">
          <Link to="/analyses" className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-700">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{analysis.filename}</h1>
            <p className="text-gray-600">Analysis #{id}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(analysis.status)}`}>
            {analysis.status.charAt(0).toUpperCase() + analysis.status.slice(1)}
          </span>
          <button className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 flex items-center gap-2">
            <Download className="w-4 h-4" />
            Export Report
          </button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Duration</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{analysis.duration}</p>
            </div>
            <Clock className="w-8 h-8 text-gray-300" />
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Detections</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{analysis.detections}</p>
            </div>
            <Video className="w-8 h-8 text-gray-300" />
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Alerts Generated</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{analysis.alerts}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-gray-300" />
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Processing Time</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">5m 22s</p>
            </div>
            <Clock className="w-8 h-8 text-gray-300" />
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Video & Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Video Player Placeholder */}
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <div className="aspect-video bg-gray-100 flex items-center justify-center relative">
              <div className="text-center">
                <Play className="w-16 h-16 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500">Annotated Video Preview</p>
                <p className="text-sm text-gray-400 mt-1">Original: {analysis.resolution} @ {analysis.fps}fps</p>
              </div>
              <div className="absolute bottom-4 right-4 bg-black/70 text-white px-3 py-1 rounded text-sm">
                {analysis.duration}
              </div>
            </div>
            <div className="p-4 border-t border-gray-200 flex items-center justify-between">
              <span className="text-sm text-gray-600">Processed: {analysis.processedFrames}/{analysis.totalFrames} frames</span>
              <button className="px-3 py-1 text-sm bg-primary-600 text-white rounded hover:bg-primary-700">
                Download Annotated
              </button>
            </div>
          </div>

          {/* Metadata */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Analysis Details</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Created</p>
                <p className="font-medium text-gray-900">{analysis.createdAt}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Completed</p>
                <p className="font-medium text-gray-900">{analysis.completedAt}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Resolution</p>
                <p className="font-medium text-gray-900">{analysis.resolution}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">FPS</p>
                <p className="font-medium text-gray-900">{analysis.fps}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">File Size</p>
                <p className="font-medium text-gray-900">{analysis.fileSize}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Model Version</p>
                <p className="font-medium text-gray-900">{analysis.modelVersion}</p>
              </div>
            </div>
          </div>

          {/* Detections by Class */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Detections by Class</h2>
            <div className="space-y-3">
              {detectionsByClass.map((d) => (
                <div key={d.class} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full bg-primary-500" />
                    <span className="capitalize font-medium text-gray-900">{d.class}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-primary-500 rounded-full" style={{ width: `${(d.count / analysis.detections) * 100}%` }} />
                    </div>
                    <span className="text-sm font-medium text-gray-900 w-12 text-right">{d.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - Alerts */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Alerts</h2>
            {alerts.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <AlertTriangle className="w-12 h-12 mx-auto text-gray-300 mb-3" />
                <p>No alerts generated</p>
              </div>
            ) : (
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className={`p-4 rounded-lg border ${getSeverityColor(alert.severity)}`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-medium text-gray-900 capitalize">{alert.type.replace('_', ' ')}</span>
                          <span className="px-2 py-0.5 text-xs rounded-full bg-white/50">
                            {alert.severity.toUpperCase()}
                          </span>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                          <span>Confidence: <span className="font-medium text-gray-900">{(alert.confidence * 100).toFixed(0)}%</span></span>
                          <span>Time: <span className="font-medium text-gray-900">{alert.timestamp}</span></span>
                          <span>Frame: <span className="font-medium text-gray-900">{alert.frame}</span></span>
                        </div>
                      </div>
                      <span className={alert.acknowledged ? 'text-green-600' : 'text-gray-400'}>
                        {alert.acknowledged ? '✓ Acknowledged' : '⏳ Pending'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Frame Thumbnails Placeholder */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Key Frames</h2>
            <div className="grid grid-cols-3 gap-2">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="aspect-video bg-gray-100 rounded flex items-center justify-center">
                  <span className="text-gray-400 text-xs">Frame {alerts[i-1]?.frame || 'N/A'}</span>
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-500 mt-3 text-center">Click to view full frame</p>
          </div>
        </div>
      </div>
    </div>
  )
}