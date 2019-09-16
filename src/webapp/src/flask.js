/*
   This module handles the Flask context,
   either set by the Meltano API in production
   or from webpack in development.
*/

module.exports = function() {
  return (
    window.FLASK || {
      appUrl: process.env.MELTANO_WEBAPP_URL,
      airflowUrl: process.env.AIRFLOW_URL
    }
  )
}