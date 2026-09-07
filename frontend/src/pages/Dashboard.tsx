import { Video, Upload, Clock, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

const stats = [
  { name: 'Total Analyses', value: '0', icon: Video, color: 'bg-blue-500' },
  { name: 'Completed', value: '0', icon: CheckCircle, color: 'bg-green-500' },
  { name: 'Processing', value: '0', icon: Clock, color: 'bg-yellow-500' },
  { name: 'Alerts Generated', value: '0', icon: AlertTriangle, color: 'bg-red-500' },
]

const quickActions = [
  { name: 'Upload Video', href: '/analyses', icon: Upload, description: 'Start a new video analysis' },
  { name: 'View History', href: '/analyses', icon: FileText, description: 'Browse previous analyses' },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Monitor and manage your video surveillance analyses</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">{stat.name}</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-full ${stat.color}`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              to={action.href}
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <div className="p-3 bg-primary-100 rounded-lg">
                <action.icon className="w-6 h-6 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="font-medium text-gray-900">{action.name}</p>
                <p className="text-sm text-gray-500">{action.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity Placeholder */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Recent Analyses</h2>
          <Link to="/analyses" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
            View All →
          </Link>
        </div>
        <div className="text-center py-8 text-gray-500">
          <Video className="w-12 h-12 mx-auto text-gray-300 mb-3" />
          <p className="text-lg font-medium">No analyses yet</p>
          <p className="text-sm mt-1">Upload your first video to get started</p>
          <Link to="/analyses" className="mt-4 inline-block text-primary-600 hover:text-primary-700 font-medium">
            Upload Video →
          </Link>
        </div>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center">
            <TrendingUp className="w-6 h-6 text-green-500 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-500">API Status</p>
              <p className="text-lg font-bold text-green-600">Healthy</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center">
            <Video className="w-6 h-6 text-blue-500 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-500">YOLO Model</p>
              <p className="text-lg font-bold text-blue-600">Not Loaded</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center">
            <TrendingUp className="w-6 h-6 text-purple-500 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-500">Classifier Model</p>
              <p className="text-lg font-bold text-purple-600">Not Trained</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}