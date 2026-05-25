'use strict';

const express = require('express');

function createUsageRouter({ usageTracker }) {
  const router = express.Router();

  router.get('/usage', (req, res) => {
    res.json(usageTracker.getSummary());
  });

  return router;
}

module.exports = { createUsageRouter };
