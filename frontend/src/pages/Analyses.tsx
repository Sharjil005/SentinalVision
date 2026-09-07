import { Video, Search, Filter, MoreVertical, Clock, CheckCircle, XCircle, AlertTriangle } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'

const mockAnalyses = [
  { id: '1', filename: 'sample_video.mp4', status: 'completed', createdAt: '2024-01-15 10:30', duration: '2:34', detections: 142, alerts: 3 },
  { id: '2', filename: 'parking_lot.avi', status: 'processing', createdAt: '2024-01-15 09:15', duration: '5:12', detections: 0, alerts: 0 },
  { id: '3', filename: 'entrance_cam.mov', status: 'failed', createdAt: '2024-01-14 16:45', duration: '1:22', detections: 0, alerts: 0 },
]

export default function Analyses() {
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredAnalyses = mockAnalyses.filter(a => {
    const matchesSearch = a.filename.toLowerCase().includes(search.toLowerCase())
    const matchesStatus = statusFilter === 'all' || a.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"><CheckCircle className="w-3 h-3 mr-1" /> Completed</span>
      case 'processing':
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800"><Clock className="w-3 h-3 mr-1" /> Processing</span>
      case 'failed':
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"><XCircle className="w-3 h-3 mr-1" /> Failed</span>
      default:
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">{status}</span>
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analyses</h1>
          <p className="text-gray-600 mt-1">Manage and review your video analyses</p>
        </div>
        <Link to="/analyses/new" className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
          <Video className="w-4 h-4 mr-2" />
          Upload Video
        </Link>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by filename..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white"
            >
              <option value="all">All Status</option>
              <option value="completed">Completed</option>
              <option value="processing">Processing</option>
              <option value="failed">Failed</option>
            </select>
          </div>
        </div>
      </div>

      {/* Analyses Table */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Video</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Detections</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Alerts</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredAnalyses.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-6 py-12 text-center text-gray-500">
                  <Video className="w-12 h-12 mx-auto text-gray-300 mb-3" />
                  <p className="text-lg font-medium">No analyses found</p>
                  <p className="text-sm mt-1">Upload a video to start your first analysis</p>
                </td>
              </tr>
            ) : (
              filteredAnalyses.map((analysis) => (
                <tr key={analysis.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <Video className="w-8 h-8 text-gray-400 mr-3" />
                      <span className="font-medium text-gray-900">{analysis.filename}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">{getStatusBadge(analysis.status)}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{analysis.createdAt}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{analysis.duration}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{analysis.detections}</td>
                  <td className="px-6 py-4">
                    {analysis.alerts > 0 ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        <AlertTriangle className="w-3 h-3 mr-1" />
                        {analysis.alerts}
                      </span>
                    ) : (
                      <span className="text-sm text-gray-600">0</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link
                      to={`/analyses/${analysis.id}`}
                      className="text-primary-600 hover:text-primary-700 font-medium"
                    >
                      View Details
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600">Showing 1 to 3 of 3 results</p>
        <div className="flex space-x-2">
          <button className="px-3 py-1 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 disabled:opacity-50" disabled>Previous</button>
          <button className="px-3 py-1 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 disabled:opacity-50" disabled>Next</button>
        </div>
      </div>
    </div>
  )
}