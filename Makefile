PUBLIC_IP = $(shell op plugin run -- aws ec2 describe-instances --filters "Name=tag:Name,Values=ebpf-sandbox" | jq -r '.Reservations[].Instances[].PublicIpAddress')
SSH_USERNAME := ec2-user
SSH = ssh $(SSH_USERNAME)@$(PUBLIC_IP)

# === remote ===
.PHONY: ssh
ssh:
	$(SSH)

.PHONY: deploy
deploy:
	rg --files | rsync -av --files-from=- . $(SSH_USERNAME)@$(PUBLIC_IP):~/poc/
	$(SSH) "cd poc && bundle install --jobs=8"
# === remote ===

# === local ===
.PHONY: run-http
run-http:
	bundle exec ruby src/test.rb

.PHONY: run-bpf
run-bpf:
	sudo -E bundle exec ruby src/poc.rb
# === local ===
