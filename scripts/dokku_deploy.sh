if ([ "$TRAVIS_PULL_REQUEST" == "false" ] && [ "$TRAVIS_BRANCH" == "production" ]); then
  echo -e "Host dartplan.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
  chmod 600 config/deploy_id_rsa
  eval `ssh-agent -s`
  ssh-add config/deploy_id_rsa
  git remote add dokku dokku@dartplan.com:dartplan
  git push dokku production
fi
